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

import socket

from threading import Thread
from logger import logln

class SocketServer:

  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.active = False
    self.receivers = []
    self.clients = []

  def setup_client(self, client: socket.socket, addr):
    self.clients.append(client)

    while self.active:
      data = client.recv(4096)

      if not data:
        break

      message = data.decode('utf-8')
      logln(f'Received from {addr} for port {self.port}: {message}')

      for receiver in self.receivers:
        receiver(message)

    self.clients.remove(client)
    client.close()

  def setup_socket(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((self.ip, self.port))
      s.listen()

      logln(f'Socket server now listening on {self.ip}:{self.port}')

      while self.active:
        client, addr = s.accept()

        t = Thread(target=self.setup_client, args=(client, addr), name=f'cl_l:{addr}')
        t.daemon = True
        t.start()

        logln(f'Accepted socket client at {addr} for port {self.port}')

      s.close()

  def start(self):
    self.active = True
    t = Thread(target=self.setup_socket, name=f'sock:{self.port}')
    t.daemon = True
    t.start()

  def stop(self):
    logln(f'Disabling socket server for {self.port}')
    self.active = False

  def sendToAll(self, message: str):
    for client in self.clients:
      client.send(message.encode('utf-8'))

  def onAnyReceive(self, receiver):
    self.receivers.append(receiver)