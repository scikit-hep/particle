# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from ..corsika import Corsika7ID
from ..pdgid import PDGID
from .bimap import BiMap

Corsika72PDGIDBiMap = BiMap(PDGID, Corsika7ID)
Corsika72PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG and Corsika7 IDs.

Examples
--------
>>> cid = Corsika72PDGIDBiMap[PDGID(-13)]
>>> cid
<Corsika7ID: 13>

>>> cid = Corsika72PDGIDBiMap[Corsika7ID(5)]
>>> cid
<PDGID: -13>
"""
