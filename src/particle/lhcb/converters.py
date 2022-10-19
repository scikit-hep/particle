# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

from ..converters.bimap import BiMap
from ..pdgid import PDGID
from . import data

LHCbName2PDGIDBiMap = BiMap(
    PDGID,
    str,
    converters=(int, str),
    filename=data.basepath / "pdgid_to_lhcbname.csv",
)
LHCbName2PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG IDs and LHCb names.

Examples
--------
>>> name = LHCbName2PDGIDBiMap[PDGID(-531)]
>>> name
'B_s~0'

>>> pdgid = LHCbName2PDGIDBiMap['B_s~0']
>>> pdgid
<PDGID: -531>
"""
