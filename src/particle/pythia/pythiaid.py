# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Class representing a Pythia ID.
"""

from __future__ import absolute_import

import csv

from .. import data
from ..exceptions import MatchingIDNotFound
from ..pdgid import PDGID

with data.basepath.joinpath("pdgid_to_pythiaid.csv").open() as _f:
    _bimap = {
        int(v["PYTHIAID"]): int(v["PDGID"])
        for v in csv.DictReader(line for line in _f if not line.startswith("#"))
    }


class PythiaID(int):
    """
    Holds a Pythia ID.

    Examples
    --------
    >>> pythiaid = PythiaID(211)

    >>> from particle import Particle
    >>> p = Particle.from_pdgid(pythiaid.to_pdgid())

    >>> p = Particle.find(pdgid=pythiaid.to_pdgid())
    >>> p.name
    'pi+'
    """

    __slots__ = ()  # Keep PythiaID a slots based class

    @classmethod
    def from_pdgid(cls, pdgid):
        # type: (int) -> PythiaID
        """
        Constructor from a PDGID.
        """
        for k, v in _bimap.items():
            if v == pdgid:
                return cls(k)
        raise MatchingIDNotFound(
            "Non-existent PythiaID for input PDGID {} !".format(pdgid)
        )

    def to_pdgid(self):
        # type: () -> PDGID
        return PDGID(_bimap[self])

    def __repr__(self):
        # type: () -> str
        return "<PythiaID: {:d}>".format(int(self))

    def __str__(self):
        # type: () -> str
        return repr(self)

    def __neg__(self):
        # type: () -> PythiaID
        return self.__class__(-int(self))

    __invert__ = __neg__
