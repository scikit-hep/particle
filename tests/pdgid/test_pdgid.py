# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest

from particle.pdgid import PDGID
from particle.pdgid.pdgid import _fnames
from particle.pdgid import functions as _functions


def test_class_string_representations():
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


def test_class_return_type():
    assert isinstance(-PDGID(311), PDGID)
    assert isinstance(~PDGID(311), PDGID)


def test_class_inversion():
    assert -PDGID(311) == ~PDGID(311)


def test_nonphysical_pdgids():
    # The negative PDGID of a self-conjugate meson makes no sense
    assert PDGID(-111).is_meson == False  # the "anti-pi0" with opposite PDGID of a pi0 does not exist
    assert PDGID(-443).is_meson == False  # the "anti-J/psi" with opposite PDGID of a J/psi does not exist


def test_info():
    __info = """A              None
C              None
J              1.0
L              None
P              None
S              None
Z              None
abspid         22
charge         0.0
has_bottom     False
has_charm      False
has_down       False
has_fundamental_anti False
has_strange    False
has_top        False
has_up         False
is_Qball       False
is_Rhadron     False
is_SUSY        False
is_baryon      False
is_diquark     False
is_dyon        False
is_hadron      False
is_lepton      False
is_meson       False
is_nucleus     False
is_pentaquark  False
is_valid       True
j_spin         3
l_spin         None
s_spin         None
three_charge   0
"""
    assert PDGID(22).info() == __info


def test_decorated_class_methods(PDGIDs):
    """
    Check that all particle.pdgid functions decorated in the PDGID class
    work as expected for all kinds of PDGIDs.
    """
    for m in _fnames:
        for pid in PDGIDs:
            assert getattr(PDGID(pid), m) == getattr(_functions, m)(pid)
