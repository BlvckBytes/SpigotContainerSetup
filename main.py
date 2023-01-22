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

from setup_spigot import setup_spigot
from bash_utils import run_bash_live
from logger import logln_error

# Prerequisites: Python3, Git

def main():
  rev = '1.18'
  jar_path = setup_spigot(rev)

  if jar_path is None:
    logln_error(f'Could not set up spigot for minecraft-revision {rev}, exiting')
    sys.exit(1)

  run_bash_live(f'java -jar {os.path.basename(jar_path)} nogui', os.path.dirname(jar_path))

if __name__ == '__main__':
  main()