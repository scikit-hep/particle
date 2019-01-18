# Licensed under a 3-clause BSD style license, see LICENSE.

import pytest

from particle.pdgid import PDGID
from particle.pdgid import functions as _functions


def test_class_methods():
    pid = PDGID(11)
    assert pid == 11
    assert pid.__str__() == '<PDGID: 11>'
    pid = PDGID(-99999999)
    assert pid.__str__() == '<PDGID: -99999999 (is_valid==False)>'

def test_class_operations(PDGIDs):
    id_electron = PDGID(PDGIDs.Electron)
    id_positron = PDGID(PDGIDs.Positron)
    assert PDGIDs.Electron == id_electron
    assert id_positron == - id_electron
    assert PDGIDs.Positron == - id_electron


def test_decorated_class_methods(PDGIDs):
    """
    Trivial check that all particle.pdgid functions decorated in the PDGID class
    work as expected for all kinds of PDGIDs.
    """
    meths = [ m for m in PDGID.__dict__ if not m.startswith('_') ]
    for m in meths:
        for pid in PDGIDs:
            assert getattr(PDGID(pid),m) == getattr(_functions,m)(pid)
