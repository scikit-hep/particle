# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle.pdgid import PDGID
from particle.pythia import PythiaID

# The only Pythia IDs differing from the standard PDG IDs,
# as (PDG ID, Pythia ID) pairs
legacy_numberings = [
    (10221, 10331),  # f(0)(1370)
    (9000111, 10111),  # a(0)(980)0
    (9000211, 10211),  # a(0)(980)+
    (-9000211, -10211),  # a(0)(980)-
    (9010221, 10221),  # f(0)(980)
]


def test_class_string_representations() -> None:
    pid = PythiaID(211)
    assert pid == 211
    assert pid.__str__() == "<PythiaID: 211>"


def test_class_return_type() -> None:
    assert isinstance(-PythiaID(211), PythiaID)
    assert isinstance(~PythiaID(211), PythiaID)


def test_class_inversion() -> None:
    assert -PythiaID(311) == ~PythiaID(311)


def test_from_pdgid() -> None:
    assert PythiaID.from_pdgid(9010221) == 10221

    assert PythiaID.from_pdgid(PDGID(9010221)) == 10221
    assert PythiaID.from_pdgid(PDGID(9010221)) == PythiaID(10221)


def test_to_pdgid() -> None:
    pythiaid = PythiaID(10331)
    assert pythiaid.to_pdgid() == 10221
    assert pythiaid.to_pdgid() == PDGID(10221)


@pytest.mark.parametrize(("pdgid", "pythiaid"), legacy_numberings)
def test_legacy_numberings(pdgid: int, pythiaid: int) -> None:
    assert PythiaID.from_pdgid(PDGID(pdgid)) == PythiaID(pythiaid)
    assert PythiaID(pythiaid).to_pdgid() == PDGID(pdgid)


@pytest.mark.parametrize("pid", [211, -211, 11, 2212, 1000010020, 9000221])
def test_identity_conversions(pid: int) -> None:
    """
    Pythia follows the standard PDG IDs apart from the few legacy numberings,
    hence conversions are the identity for everything else.
    """
    assert PythiaID.from_pdgid(PDGID(pid)) == PythiaID(pid)
    assert PythiaID(pid).to_pdgid() == PDGID(pid)
