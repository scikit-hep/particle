# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle.exceptions import MatchingIDNotFound
from particle.geant import Geant3ID
from particle.pdgid import PDGID


def test_class_string_representations():
    pid = Geant3ID(1)
    assert pid == 1
    assert pid.__str__() == "<Geant3ID: 1>"


def test_class_return_type():
    assert isinstance(-Geant3ID(3), Geant3ID)
    assert isinstance(~Geant3ID(3), Geant3ID)


def test_class_inversion():
    assert -Geant3ID(1) == ~Geant3ID(1)


def test_from_pdgid():
    assert Geant3ID.from_pdgid(211) == 8

    assert Geant3ID.from_pdgid(PDGID(211)) == 8
    assert Geant3ID.from_pdgid(PDGID(211)) == Geant3ID(8)


def test_from_pdgid_non_matching():
    with pytest.raises(MatchingIDNotFound):
        Geant3ID.from_pdgid(55)


def test_to_pdgid():
    gid = Geant3ID(8)
    assert gid.to_pdgid() == 211
    assert gid.to_pdgid() == PDGID(211)
