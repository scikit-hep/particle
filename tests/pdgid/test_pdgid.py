# Licensed under a 3-clause BSD style license, see LICENSE.

import pytest

from particle.pdgid import PDGID
from particle.pdgid import functions as _functions


def test_class_methods():
    id = PDGID(11)
    assert id.pdgid == 11
    assert id.__str__() == '<PDGID: 11>'
    id = PDGID(-99999999)
    assert id.__str__() == '<PDGID: -99999999 (is_valid==False)>'


def test_decorated_class_methods(PDGIDs):
    """
    Trivial check that all particle.pdgid functions decorated in the PDGID class
    work as expected for all kinds of PDGIDs.
    """
    meths = [ m for m in PDGID.__dict__ if not m.startswith('_') ]
    for m in meths:
        for id in PDGIDs:
            assert getattr(PDGID(id),m) == getattr(_functions,m)(id)
