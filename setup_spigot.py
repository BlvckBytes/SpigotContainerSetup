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
import sys

from tqdm import tqdm
from bash_utils import run_bash_live
from tqdm_wrapper import tqdm_wrapper
from logger import logln, logln_error

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