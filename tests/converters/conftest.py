# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle.converters import (
    Corsika72PDGIDBiMap,
    Geant2PDGIDBiMap,
    Pythia2PDGIDBiMap,
)


@pytest.fixture(autouse=True)
def _reset_deprecation_state() -> None:
    """
    The deprecated BiMaps warn only once per object, but they are
    module-level singletons whose state would otherwise leak across tests.
    Reset it before every test so the warning is observable deterministically.
    """
    for bimap in (Corsika72PDGIDBiMap, Geant2PDGIDBiMap, Pythia2PDGIDBiMap):
        bimap._warned = False
