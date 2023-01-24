"""
MIT License

Copyright (c) 2023 BlvckBytes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess
import os

from socket_server import SocketServer
from setup_spigot import setup_spigot
from logger import logln_error, logln
from threading import Thread

def process_listener(process: subprocess.Popen, server: SocketServer):
  while process.returncode is None:
    line = process.stdout.readline()

    if line is None or len(line) == 0:
      break

    message = line.decode('utf-8')
    logln(f'Received from STDOUT: {message.strip()}')
    server.sendToAll(message)

  server.stop()

def relay_socket_message(message, process: subprocess.Popen):
  process.stdin.write(message.encode('utf-8'))
  process.stdin.flush()
  logln(f'Wrote to STDIN: {message}')

def socket_terminal(rev, port):
  """
  Sets up the provided minecraft-revision of spigot and spawns the process in a terminal
  which communicates over a socket connection

  :return: SocketServer instance on success, None on failure
  """

  jar_path = setup_spigot(rev)

  if jar_path is None:
    logln_error(f'Could not set up spigot for minecraft-revision {rev}, exiting')
    return None

  process = subprocess.Popen(
    f'java -jar {os.path.basename(jar_path)} nogui'.split(),
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=os.path.dirname(jar_path)
  )

  server = SocketServer('0.0.0.0', port)
  server.start()
  server.onAnyReceive(lambda message: relay_socket_message(message, process))

  t = Thread(target=process_listener, args=(process, server), name=f'proc_l:{rev}')

  t.daemon = True
  t.start()
  return server