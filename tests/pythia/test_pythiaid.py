# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle.exceptions import MatchingIDNotFound
from particle.pdgid import PDGID
from particle.pythia import PythiaID


def test_class_string_representations():
    pid = PythiaID(211)
    assert pid == 211
    assert pid.__str__() == "<PythiaID: 211>"


def test_class_return_type():
    assert isinstance(-PythiaID(211), PythiaID)
    assert isinstance(~PythiaID(211), PythiaID)


def test_class_inversion():
    assert -PythiaID(311) == ~PythiaID(311)


def test_from_pdgid():
    assert PythiaID.from_pdgid(9010221) == 10221

    assert PythiaID.from_pdgid(PDGID(9010221)) == 10221
    assert PythiaID.from_pdgid(PDGID(9010221)) == PythiaID(10221)

    with pytest.raises(MatchingIDNotFound):
        PythiaID.from_pdgid(9000221)


def test_to_pdgid():
    pythiaid = PythiaID(10331)
    assert pythiaid.to_pdgid() == 10221
    assert pythiaid.to_pdgid() == PDGID(10221)
