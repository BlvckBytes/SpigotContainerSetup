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

import sys
import time

from socket_terminal import socket_terminal
from logger import logln_error

def main():
  if len(sys.argv) != 3:
    logln_error(f'Usage: {sys.argv[0]} <rev> <socket_port>')
    sys.exit(1)

  server = socket_terminal(sys.argv[1], int(sys.argv[2]))

  if server is None:
    sys.exit(1)

  # Maybe add a terminal here in the future, just block for now
  # FIXME: Properly stopping the minecraft- as well as the socket-server
  while server.active:
    time.sleep(.1)

if __name__ == '__main__':
  main()