# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from ..geant import Geant3ID
from ..pdgid import PDGID
from .bimap import BiMap

Geant2PDGIDBiMap = BiMap(PDGID, Geant3ID)
Geant2PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG and Geant3 IDs.

Examples
--------
>>> gid = Geant2PDGIDBiMap[PDGID(211)]
>>> gid
<Geant3ID: 8>

>>> pdgid = Geant2PDGIDBiMap[Geant3ID(8)]
>>> pdgid
<PDGID: 211>
"""
