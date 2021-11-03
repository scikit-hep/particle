# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from ...converters.bimap import BiMap
from ...pdgid import PDGID
from .. import data

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
