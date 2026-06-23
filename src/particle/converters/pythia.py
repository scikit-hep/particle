# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from ..pdgid import PDGID
from ..pythia import PythiaID
from .bimap import _DeprecatedBiMap

Pythia2PDGIDBiMap = _DeprecatedBiMap(PDGID, PythiaID, name="Pythia2PDGIDBiMap")
Pythia2PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG and Pythia IDs.

.. deprecated:: 1.0.0
    Use ``PythiaID.from_pdgid()`` and ``PythiaID.to_pdgid()`` instead.

Examples
--------
>>> pyid = Pythia2PDGIDBiMap[PDGID(9010221)]  # doctest: +SKIP
>>> pyid  # doctest: +SKIP
<PythiaID: 10221>

>>> pdgid = Pythia2PDGIDBiMap[PythiaID(10221)]  # doctest: +SKIP
>>> pdgid  # doctest: +SKIP
<PDGID: 9010221>
"""
