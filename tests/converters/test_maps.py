# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle import data
from particle.converters.bimap import BiMap, DirectionalMaps
from particle.exceptions import MatchingIDNotFound
from particle.geant import Geant3ID
from particle.pdgid import PDGID


def test_BiMap() -> None:
    bimap = BiMap(PDGID, Geant3ID)

    assert len(bimap) == 945
    assert "BiMap(PDGID-Geant3ID)" in str(bimap)

    with pytest.raises(MatchingIDNotFound):
        bimap[PDGID(998877)]


def test_DirectionalMaps() -> None:
    filename = data.basepath / "pdgid_to_geant3id.csv"
    PDG2GeantIDMap, Geant2PDGIDMap = DirectionalMaps(
        "PDGID", "Geant3ID", filename=filename, converters=(int, int)
    )

    assert len(PDG2GeantIDMap) == 945
    assert len(Geant2PDGIDMap) == 945

    assert "DirectionalMap(PDGID->GEANT3ID)" in str(PDG2GeantIDMap)
    assert "DirectionalMap(GEANT3ID->PDGID)" in str(Geant2PDGIDMap)

    with pytest.raises(MatchingIDNotFound):
        PDG2GeantIDMap[PDGID(998877)]
    with pytest.raises(MatchingIDNotFound):
        Geant2PDGIDMap[Geant3ID(998877)]
