"""
MIT License

Copyright (c) 2023 BlvckBytes, leimao

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

# Excerpt from: https://gist.github.com/leimao/37ff6e990b3226c2c9670a2cd1e4a6f5

def tqdm_wrapper(t):
  """Wraps tqdm instance.
  Don't forget to close() or __exit__()
  the tqdm instance once you're done with it (easiest using `with` syntax).
  Example
  -------
  >>> with tqdm(...) as t:
  ...     reporthook = my_hook(t)
  ...     urllib.urlretrieve(..., reporthook=reporthook)
  """
  last_b = [0]

  def update_to(b=1, bsize=1, tsize=None):
    """
    b  : int, optional
        Number of blocks transferred so far [default: 1].
    bsize  : int, optional
        Size of each block (in tqdm units) [default: 1].
    tsize  : int, optional
        Total size (in tqdm units). If [default: None] remains unchanged.
    """
    if tsize is not None:
        t.total = tsize
    t.update((b - last_b[0]) * bsize)
    last_b[0] = b

  return update_to