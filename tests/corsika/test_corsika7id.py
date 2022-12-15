from __future__ import annotations

import pytest

from particle.corsika import Corsika7ID
from particle.exceptions import MatchingIDNotFound
from particle.pdgid import PDGID


def test_class_string_representations():
    pid = Corsika7ID(1)
    assert pid == 1
    assert pid.__str__() == "<Corsika7ID: 1>"


def test_class_return_type():
    assert isinstance(Corsika7ID(3), Corsika7ID)


def test_from_pdgid():
    assert Corsika7ID.from_pdgid(-13) == 5

    assert Corsika7ID.from_pdgid(PDGID(-13)) == 5
    assert Corsika7ID.from_pdgid(PDGID(13)) == Corsika7ID(6)


def test_from_pdgid_non_matching():
    with pytest.raises(MatchingIDNotFound):
        Corsika7ID.from_pdgid(55)


def test_to_pdgid():
    cid = Corsika7ID(5)
    assert cid.to_pdgid() == -13
    assert cid.to_pdgid() == PDGID(-13)


def test_is_particle():
    cid = Corsika7ID(1)
    assert cid.is_particle()
    cid = Corsika7ID(75)
    assert not cid.is_particle()


def test_from_particle_description():
    cid, is_mother = Corsika7ID.from_particle_description(-6001)
    assert is_mother
    assert cid.is_particle()
    cid, is_mother = Corsika7ID.from_particle_description(75001)
    assert not is_mother
    assert not cid.is_particle()
