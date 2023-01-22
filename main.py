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

import os
import sys

from setup_java import setup_java
from setup_spigot import build_spigot
from bash_utils import run_bash_live
from logger import logln_error

# Prerequisites: Python3, Git

def accept_eula(server_dir):
  """
  Creates or overrides eula.txt at the provided directory so that it contains an eula accepting statement

  :param str server_dir: Path of the folder where the server is executed at
  """

  with open(os.path.join(server_dir, 'eula.txt'), 'w') as f:
    f.write('eula=true\n')

def main():
  home_dir = os.path.expanduser('~')
  server_dir = os.path.join(home_dir, 'spigot')

  if not os.path.isdir(server_dir):
    os.mkdirs(server_dir)

  if not setup_java(16):
    logln_error(f'Could not set up the required java version, exiting')
    sys.exit(1)

  jar_path = build_spigot('1.17', server_dir)

  if jar_path is None:
    logln_error(f'Could not build the required spigot jar, exiting')
    sys.exit(1)

  accept_eula(server_dir)

  run_bash_live(f'java -jar {jar_path} nogui', server_dir)

if __name__ == '__main__':
  main()