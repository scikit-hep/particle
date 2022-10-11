# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from .corsika import Corsika72PDGIDBiMap
from .evtgen import EvtGen2PDGNameMap, EvtGenName2PDGIDBiMap, PDG2EvtGenNameMap
from .geant import Geant2PDGIDBiMap
from .pythia import Pythia2PDGIDBiMap

__all__ = (
    "EvtGen2PDGNameMap",
    "EvtGenName2PDGIDBiMap",
    "PDG2EvtGenNameMap",
    "Geant2PDGIDBiMap",
    "Pythia2PDGIDBiMap",
    "Corsika72PDGIDBiMap",
)


def __dir__() -> tuple[str, ...]:
    return __all__
