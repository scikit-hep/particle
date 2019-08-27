# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

import csv

from .. import data
from ..exceptions import MatchingIDNotFound


class BiMap(object):
    """
    Bi-bidirectional map class.

    Examples
    --------
    >>> bimap = BiMap(PDGID, PythiaID)
    >>> bimap[PDGID(9010221)]
    <PythiaID: 10221>
    >>> bimap[PythiaID(10221)]
    <PDGID: 9010221>
    """
    def __init__(self, class_A, class_B, filename=None):
        self.__A = class_A
        self.__B = class_B
        name_A = self.__A.__name__.upper()
        name_B = self.__B.__name__.upper()
        if not filename:
            filename = '{a}_to_{b}.csv'.format(a=name_A.lower(), b=name_B.upper())
        with data.open_text(data, filename) as _f:
            self._to_map = {int(v[name_B]):int(v[name_A]) for v in csv.DictReader(_f)}
            _f.seek(0)
            self._from_map = {int(v[name_A]):int(v[name_B]) for v in csv.DictReader(_f)}

    def __getitem__(self, value):
        if isinstance(value, self.__B):
            try:
                return self.__A(self._to_map[value])
            except KeyError:
                pass
        elif isinstance(value, self.__A):
            try:
                return self.__B(self._from_map[value])
            except KeyError:
                pass
        msg = "Matching {a}-{b} for input {v} not found !".format(
              a=self.__A.__name__, b=self.__B.__name__, v=value)
        raise MatchingIDNotFound(msg)

    def __len__(self):
        """Returns the number of matches."""
        return len(self._to_map)
