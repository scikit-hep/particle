# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from .. import data

from ..pdgid import PDGID

from .bimap import BiMap, DirectionalMaps


EvtGenName2PDGIDBiMap = BiMap(
    PDGID,
    str,
    converters=(int, str),
    filename=data.open_text(data, "pdgid_to_evtgenname.csv"),
)
EvtGenName2PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG IDs and EvtGen names.

Examples
--------
>>> name = EvtGenName2PDGIDBiMap[PDGID(22)]
>>> name
'gamma'

>>> pdgid = EvtGenName2PDGIDBiMap['gamma']
>>> pdgid
<PDGID: 22>
"""


PDG2EvtGenNameMap, EvtGen2PDGNameMap = DirectionalMaps("PDGName", "EvtGenName")

PDG2EvtGenNameMap.__doc__ = """
Directional map between PDG and EvtGen names.

Examples
--------
>>> PDG2EvtGenNameMap['J/psi(1S)']
'J/psi'
"""


EvtGen2PDGNameMap.__doc__ = """
Directional map between EvtGen and names.

Examples
--------
>>> EvtGen2PDGNameMap['J/psi']
>>> 'J/psi(1S)'
"""

del BiMap
del DirectionalMaps
