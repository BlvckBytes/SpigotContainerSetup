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

import urllib.request
import os

from tqdm import tqdm
from bash_utils import run_bash_live
from tqdm_wrapper import tqdm_wrapper
from logger import logln, logln_error
from setup_java import setup_java

def build_spigot(rev, output_dir):
  """
  Downloads the BuildTools JAR file into a temporary directory and invokes it by passing
  the desired revision as well as the output directory path as arguments

  :param str rev: Revision of the minecraft server (1.8, 1.9, 1.17, ...)
  :param str output_dir: Output directory to put the final JAR file into
  :return: Final JAR path on success, None on errors
  """

  container_dir = '/tmp/BuildTools'

  if not os.path.isdir(container_dir):
    os.makedirs(container_dir)

  if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

  jar_path = os.path.join(container_dir, 'BuildTools.jar')
  output_path = os.path.join(output_dir, f'spigot-{rev}.jar')

  if os.path.isfile(output_path):
    logln(f'Jar for revision {rev} already existed')
    return output_path

  if not os.path.isfile(jar_path):
    buildtools_url = 'https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar'

    logln(f'BuildTools does not yet exist at {jar_path}, downloading...')
    with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc='') as t:
      urllib.request.urlretrieve(buildtools_url, jar_path, tqdm_wrapper(t))

    logln('BuildTools download finished')

  exit_code = run_bash_live(f'java -jar BuildTools.jar --rev {rev} --output-dir={output_dir}', container_dir)

  if exit_code != 0:
    logln_error(f'BuildTools yielded invalid exit-code {exit_code}')
    return None

  if not os.path.isfile(output_path):
    logln_error(f'Could not locate output jar in directory {output_dir}')
    return None

  logln(f'Jar successfully built and written into {output_dir}')
  return output_path

def decide_java_version(rev):
  """
  Decides the required java version for a given minecraft revision of format major.minor.build

  :return: Java major version integer on success, None if the version could not be decided
  """

  version_strings = rev.split('.', 3)
  major = int(version_strings[0])
  minor = int(version_strings[1])

  # Currently not interested in this information
  # build = int(version_strings[2] if len(version_strings) == 3 else 0)

  if major != 1:
    return None

  if minor == 19:
    return 18

  if minor == 18:
    return 17

  if minor == 17:
    return 16

  if minor <= 16 and minor >= 8:
    return 11

  return None

def accept_eula(server_dir):
  """
  Creates or overrides eula.txt at the provided directory so that it contains an eula accepting statement

  :param str server_dir: Path of the folder where the server is executed at
  """

  with open(os.path.join(server_dir, 'eula.txt'), 'w') as f:
    f.write('eula=true\n')

def delete_world_locks(server_dir):
  """
  It could happen that the server was exited non-gracefully, which left a world lock file. Delete those.

  :param str server_dir: Path of the folder where the server is executed at
  """

  run_bash_live('rm -f world*/session.lock', server_dir)

def setup_spigot(rev):
  """
  Installs the required java version, builds the required spigot JAR file and finally accepts the EULA

  :return: Server JAR file path on success, None on errors
  """

  java_version = decide_java_version(rev)
  if java_version is None:
    logln_error(f'Could not decide on a java-version for minecraft-revision {rev}')
    return None

  home_dir = os.path.expanduser('~')
  server_dir = os.path.join(home_dir, f'spigot-{rev}')

  if not os.path.isdir(server_dir):
    os.makedirs(server_dir)

  if not setup_java(java_version):
    logln_error(f'Could not set up the required java version, exiting')
    return None

  jar_path = build_spigot(rev, server_dir)

  if jar_path is None:
    logln_error(f'Could not build the required spigot jar for minecraft-revision {rev}, exiting')
    return None

  accept_eula(server_dir)
  delete_world_locks(server_dir)
  return jar_path