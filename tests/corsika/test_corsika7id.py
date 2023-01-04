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
        _ = Corsika7ID.from_pdgid(55)


def test_to_pdgid():
    cid = Corsika7ID(5)
    assert cid.to_pdgid() == -13
    assert cid.to_pdgid() == PDGID(-13)


def test_to_pdgid_invalid():
    from particle.particle import InvalidParticle  # pylint: disable=C0415

    with pytest.raises(InvalidParticle):
        _ = Corsika7ID(75).to_pdgid()


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

    # Corsika ID 201 is deuteron
    assert Corsika7ID.from_particle_description(-201000)[0].name() == "D2"


def test_from_particle_description_non_valid():
    with pytest.raises(MatchingIDNotFound):
        _ = Corsika7ID.from_particle_description(0)


def test__is_non_particle_id():
    # Muons
    assert not Corsika7ID._is_non_particle_id(5)
    assert not Corsika7ID._is_non_particle_id(6)
    # Additional muon info, which is not a particle
    assert Corsika7ID._is_non_particle_id(75)
    assert Corsika7ID._is_non_particle_id(76)
    # Weights of the MULTITHIN option
    assert Corsika7ID._is_non_particle_id(8888420)
    # Cherenkov photons on output file
    assert Corsika7ID._is_non_particle_id(9900)


def test_name():
    # check name from pdgid module
    cid = Corsika7ID(5)
    assert cid.name() == "mu+"

    # check name for non-particles
    cid = Corsika7ID(8888420)
    assert cid.name() == "weights of preceding particle (MULTITHIN option)"

    cid = Corsika7ID(9900)
    assert cid.name() == "Cherenkov photons on particle output file"

    cid = Corsika7ID(85)
    assert cid.name() == "decaying μ+ at start"


def test_name_invalid():
    from particle.particle import InvalidParticle  # pylint: disable=C0415

    with pytest.raises(InvalidParticle):
        _ = Corsika7ID(0).name()
