# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import warnings

import pytest

from particle import PDGID, Corsika7ID, Geant3ID, PythiaID
from particle.converters import (
    Corsika72PDGIDBiMap,
    Geant2PDGIDBiMap,
    Pythia2PDGIDBiMap,
)
from particle.exceptions import MatchingIDNotFound

# (deprecated BiMap, PDGID, matching MC ID)
cases = [
    (Pythia2PDGIDBiMap, PDGID(9010221), PythiaID(10221)),
    (Geant2PDGIDBiMap, PDGID(211), Geant3ID(8)),
    (Corsika72PDGIDBiMap, PDGID(-13), Corsika7ID(5)),
]


@pytest.mark.parametrize(("bimap", "pdgid", "mcid"), cases)
def test_deprecated_bimap_warns_once_and_converts(bimap, pdgid, mcid) -> None:  # type: ignore[no-untyped-def]
    # The first look-up warns and still returns the correct value...
    with pytest.warns(DeprecationWarning, match="deprecated"):
        assert bimap[pdgid] == mcid

    # ...all further look-ups are silent (turned into errors here to be sure).
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert bimap[mcid] == pdgid


def test_deprecated_bimap_preserves_pythia_whitelist() -> None:
    # The deprecated map keeps the old whitelist behavior (unlike the new,
    # algorithmic PythiaID.from_pdgid, which converts unknown IDs by identity).
    with (
        pytest.warns(DeprecationWarning, match="deprecated"),
        pytest.raises(MatchingIDNotFound),
    ):
        _ = Pythia2PDGIDBiMap[PDGID(9000221)]
