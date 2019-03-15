# Licensed under a 3-clause BSD style license, see LICENSE.

try:
    from importlib.resources import open_text
except ImportError:
    from importlib_resources import open_text
