# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from .. import data
from ..pdgid import PDGID
from .bimap import BiMap, DirectionalMaps

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
>>> name = LHCbName2PDGIDBiMap[PDGID(22)]
>>> name
'gamma'

>>> pdgid = LHCbName2PDGIDBiMap['gamma']
>>> pdgid
<PDGID: 22>
"""


PDG2LHCbNameMap, LHCb2PDGNameMap = DirectionalMaps("PDGName", "LHCbName")

PDG2LHCbNameMap.__doc__ = """
Directional map between PDG and LHCb names.

Examples
--------
>>> PDG2LHCbNameMap['J/psi(1S)']
'J/psi'
"""


LHCb2PDGNameMap.__doc__ = """
Directional map between LHCb and names.

Examples
--------
>>> LHCb2PDGNameMap['J/psi']
>>> 'J/psi(1S)'
"""

del BiMap
del DirectionalMaps
