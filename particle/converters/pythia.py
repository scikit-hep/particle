# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

import csv

from .. import data
from ..exceptions import MatchingIDNotFound
from ..pdgid import PDGID
from ..pythia import PythiaID


class __Pythia2PDGIDBiMap(object):
    """
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
    def __init__(self):
        with data.open_text(data, 'pdgid_to_pythiaid.csv') as _f:
            self._to_map = {int(v['PYTHIAID']):int(v['PDGID']) for v in csv.DictReader(_f)}
            _f.seek(0)
            self._from_map = {int(v['PDGID']):int(v['PYTHIAID']) for v in csv.DictReader(_f)}

    def __getitem__(self, value):
        if isinstance(value, PythiaID):
            return PDGID(self._to_map[value])
        elif isinstance(value, PDGID):
            return PythiaID(self._from_map[value])
        raise MatchingIDNotFound("Matching PDGID-PythiaID for input {0} not found !".format(value))

    def __len__(self):
        """Returns the number of connections."""
        return len(self._to_map)


Pythia2PDGIDBiMap = __Pythia2PDGIDBiMap()
