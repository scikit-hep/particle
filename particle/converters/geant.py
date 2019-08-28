# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from ..pdgid import PDGID
from ..geant import GeantID

from .bimap import BiMap


Geant2PDGIDBiMap = BiMap(PDGID, GeantID)
Geant2PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG and Geant IDs.

Examples
--------
>>> gid = Geant2PDGIDBiMap[PDGID(211)]
>>> gid
<GeantID: 8>

>>> pdgid = Geant2PDGIDBiMap[GeantID(8)]
>>> pdgid
<PDGID: 211>
"""
