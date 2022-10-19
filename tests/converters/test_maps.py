# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle import data
from particle.converters.bimap import BiMap, DirectionalMaps
from particle.exceptions import MatchingIDNotFound
from particle.pdgid import PDGID
from particle.pythia import PythiaID


def test_BiMap():
    bimap = BiMap(PDGID, PythiaID)

    assert len(bimap) == 540
    assert "BiMap(PDGID-PythiaID)" in str(bimap)

    with pytest.raises(MatchingIDNotFound):
        bimap[PDGID(9000221)]


def test_DirectionalMaps():
    filename = data.basepath / "pdgid_to_pythiaid.csv"
    PDG2PyIDMap, Py2PDGIDMap = DirectionalMaps(
        "PDGID", "PythiaID", filename=filename, converters=(int, int)
    )

    assert len(PDG2PyIDMap) == 540
    assert len(Py2PDGIDMap) == 540

    assert "DirectionalMap(PDGID->PYTHIAID)" in str(PDG2PyIDMap)
    assert "DirectionalMap(PYTHIAID->PDGID)" in str(Py2PDGIDMap)

    with pytest.raises(MatchingIDNotFound):
        PDG2PyIDMap[PDGID(9000221)]
    with pytest.raises(MatchingIDNotFound):
        Py2PDGIDMap[PythiaID(9000221)]
