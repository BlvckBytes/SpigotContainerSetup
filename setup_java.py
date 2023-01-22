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
import glob
import platform
import requests
import os
import tarfile

from tqdm import tqdm
from logger import logln, logln_error
from bash_utils import run_bash

def get_jdk_url(version, arch):
  """
  Get the download-url for a compressed tar-ball corresponding to a specific java major version

  :param int version: Java major version (18, 17, 16, 11, 8)
  :param str arch: Architecture string (aarch64, arm, x64)
  """

  if version == 18:
    return f'https://github.com/adoptium/temurin18-binaries/releases/download/jdk-18.0.1%2B10/OpenJDK18U-jdk_{arch}_linux_hotspot_18.0.1_10.tar.gz'

  if version == 17:
    return f'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.1%2B12/OpenJDK17U-jdk_{arch}_linux_hotspot_17.0.1_12.tar.gz'

  if version == 16:
    return f'https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_{arch}_linux_hotspot_16.0.2_7.tar.gz'

  if version == 11:
    return f'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.13%2B8/OpenJDK11U-jdk_{arch}_linux_hotspot_11.0.13_8.tar.gz'

  if version == 8:
    return f'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u312-b07/OpenJDK8U-jdk_{arch}_linux_hotspot_8u312b07.tar.gz'

  print(f'Invalid java version requested: {version}', file=sys.stderr)
  sys.exit(1)

def get_jdk_path(version):
  """
  Get the absolute path of the containing folder for a specific JDK version on the system

  :param int version: Java major version in question
  """

  matches = glob.glob(f'/usr/lib/jvm/jdk-{version}*')
  return None if len(matches) == 0 else matches[0]

def decide_system_architecture():
  machine = platform.machine().lower()

  if machine == 'arm64':
    return 'arm'

  if machine == 'aarch64':
    return 'aarch64'

  logln_error(f'Unsupported system architecture: {machine}')
  sys.exit(1)

def setup_java(version):
  """
  Setup the provided java version as the default JVM
  """

  arch = decide_system_architecture()
  jdk_path = get_jdk_path(version)

  if jdk_path is None:
    logln(f'JDK {version} not yet downloaded, initializing download...')
    jdk_url = get_jdk_url(version, arch)

    with requests.get(jdk_url, stream=True) as rx:
      # check header to get content length, in bytes
      total_length = int(rx.headers.get("Content-Length"))

      # Wrap GET stream file-like object's read to track it's progress
      # Ideally, since requests.get() is called with stream=True, downloading and extracting should
      # run in a cut-through manner, so this progress should represent downloading and extraction
      with tqdm.wrapattr(rx.raw, 'read', total=total_length, desc='') as wrapped_raw:

        # Extract the .tar.gz file into the JVM folder
        with tarfile.open(fileobj=wrapped_raw, mode='r:gz') as tar:
          tar.extractall('/usr/lib/jvm')

    logln(f'JDK {version} download finished')

  jdk_path = get_jdk_path(version)

  if jdk_path is None:
    logln_error(f'Could not find JDK {version} on the system')
    sys.exit(1)

  logln(f'Setting JDK {version} as a default')

  # Update the link to the java binary
  run_bash('rm -f /usr/bin/java')
  cout, cerr = run_bash(f'ln -s {os.path.join(jdk_path, "bin/java")} /usr/bin/java')

  if len(cerr) != 0:
    logln_error(f'Could not link JDK {version} as a default!')
    sys.exit(1)