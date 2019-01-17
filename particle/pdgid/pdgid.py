# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Class representing a PDGID.

All methods of HepPID are implemented in a Pythonic version, see the functions module.
"""

from __future__ import absolute_import

from . import functions as _functions


class PDGID(object):
    """
    Holds a PDGID.

    Example
    -------
    >>> PDGID(11).is_lepton
    True
    """
    def __init__(self, pdgid):
        self.pdgid = pdgid

    def __repr__(self):
        return "<PDGID: {:d}{:s}>".format(self.pdgid,'' if self.is_valid else ' (is_valid==False)')

# Decorate the PDGID class with all relevant functions defined in the pdgid.functions module
_exclude = ('IntEnum', 'Location', 'print_function', 'division', 'absolute_import')
_fname = [ fname for fname in dir(_functions) if not fname.startswith('_') and fname not in _exclude]
for _n in _fname:
    _decorator = property( lambda self, meth=getattr(_functions, _n) : meth(self.pdgid) )
    setattr(PDGID, _n, _decorator)
