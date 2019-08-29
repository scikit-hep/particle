# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from .. import data

from ..pdgid import PDGID

from .bimap import BiMap


EvtGenName2PDGIDBiMap = BiMap(PDGID, str,
                              converters=(int,str),
                              filename=data.open_text(data, 'pdgid_to_evtgenname.csv'))
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
