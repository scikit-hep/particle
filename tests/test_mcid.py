# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

from typing import ClassVar

import pytest

from particle.exceptions import MatchingIDNotFound
from particle.mcid import MCParticleID
from particle.pdgid import PDGID


class CustomID(MCParticleID):
    _to_pdg_map: ClassVar = {1: 11, 2: -11, 3: 22}


class OtherCustomID(MCParticleID):
    _to_pdg_map: ClassVar = {1: 13, 2: -13}


class IncompleteID(MCParticleID):
    pass


def test_class_string_representations() -> None:
    cid = CustomID(1)
    assert cid == 1
    assert cid.__str__() == "<CustomID: 1>"
    assert repr(cid) == "<CustomID: 1>"


def test_to_pdgid() -> None:
    assert CustomID(3).to_pdgid() == 22
    assert CustomID(3).to_pdgid() == PDGID(22)
    assert isinstance(CustomID(3).to_pdgid(), PDGID)


def test_to_pdgid_non_matching() -> None:
    with pytest.raises(MatchingIDNotFound):
        _ = CustomID(99).to_pdgid()


def test_from_pdgid() -> None:
    assert CustomID.from_pdgid(-11) == 2
    assert CustomID.from_pdgid(PDGID(-11)) == CustomID(2)
    assert isinstance(CustomID.from_pdgid(PDGID(-11)), CustomID)


def test_from_pdgid_non_matching() -> None:
    with pytest.raises(MatchingIDNotFound):
        _ = CustomID.from_pdgid(99)


def test_subclasses_do_not_share_conversion_maps() -> None:
    assert CustomID.from_pdgid(11) == CustomID(1)
    assert OtherCustomID.from_pdgid(13) == OtherCustomID(1)

    assert CustomID(1).to_pdgid() == PDGID(11)
    assert OtherCustomID(1).to_pdgid() == PDGID(13)

    with pytest.raises(MatchingIDNotFound):
        _ = OtherCustomID.from_pdgid(11)


def test_subclass_without_conversion_map() -> None:
    with pytest.raises(NotImplementedError, match="IncompleteID"):
        _ = IncompleteID(5).to_pdgid()

    with pytest.raises(NotImplementedError, match="IncompleteID"):
        _ = IncompleteID.from_pdgid(11)
