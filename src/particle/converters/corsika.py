# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from ..corsika import Corsika7ID
from ..pdgid import PDGID
from .bimap import _DeprecatedBiMap

Corsika72PDGIDBiMap = _DeprecatedBiMap(PDGID, Corsika7ID, name="Corsika72PDGIDBiMap")
Corsika72PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG and Corsika7 IDs.

.. deprecated:: 1.0.0
    Use ``Corsika7ID.from_pdgid()`` and ``Corsika7ID.to_pdgid()`` instead.

Examples
--------
>>> cid = Corsika72PDGIDBiMap[PDGID(-13)]  # doctest: +SKIP
>>> cid  # doctest: +SKIP
<Corsika7ID: 13>

>>> cid = Corsika72PDGIDBiMap[Corsika7ID(5)]  # doctest: +SKIP
>>> cid  # doctest: +SKIP
<PDGID: -13>
"""
