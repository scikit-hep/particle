# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

from particle import PDGID, Corsika7ID, Particle
from particle.converters import Corsika72PDGIDBiMap


def test_Corsika72PDGID():
    pdgid = Corsika72PDGIDBiMap[Corsika7ID(5)]
    assert pdgid == -13

    cid = Corsika72PDGIDBiMap[PDGID(13)]
    assert cid.is_particle()
    assert cid == 6

    p = Particle.from_pdgid(cid.to_pdgid())
    # should be muon
    assert p.charge == -1
