# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import absolute_import

# Convenient access to the version number
from .version import __version__

try:
    from importlib.resources import open_text
except ImportError:
    from importlib_resources import open_text


def get_pdt_csv(csv='mass_width_2008.csv'):
    return open_text('particle.data', csv)
