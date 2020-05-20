# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from ..pdgid import PDGID
from ..pythia import PythiaID

from .bimap import BiMap


Pythia2PDGIDBiMap = BiMap(PDGID, PythiaID)
Pythia2PDGIDBiMap.__doc__ = """
Bi-bidirectional map between PDG and Pythia IDs.

Examples
--------
>>> pyid = Pythia2PDGIDBiMap[PDGID(9010221)]
>>> pyid
<PythiaID: 10221>

>>> pdgid = Pythia2PDGIDBiMap[PythiaID(10221)]
>>> pdgid
<PDGID: 9010221>
"""
