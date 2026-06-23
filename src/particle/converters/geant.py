# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from ..geant import Geant3ID
from ..pdgid import PDGID
from .bimap import _DeprecatedBiMap

Geant2PDGIDBiMap = _DeprecatedBiMap(PDGID, Geant3ID, name="Geant2PDGIDBiMap")
Geant2PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG and Geant3 IDs.

.. deprecated:: 1.0.0
    Use ``Geant3ID.from_pdgid()`` and ``Geant3ID.to_pdgid()`` instead.

Examples
--------
>>> gid = Geant2PDGIDBiMap[PDGID(211)]  # doctest: +SKIP
>>> gid  # doctest: +SKIP
<Geant3ID: 8>

>>> pdgid = Geant2PDGIDBiMap[Geant3ID(8)]  # doctest: +SKIP
>>> pdgid  # doctest: +SKIP
<PDGID: 211>
"""
