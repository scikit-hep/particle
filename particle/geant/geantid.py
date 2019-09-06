# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Class representing a Geant ID.
"""

from __future__ import absolute_import

import csv

from .. import data
from ..pdgid import PDGID
from ..exceptions import MatchingIDNotFound


with data.open_text(data, 'pdgid_to_geantid.csv') as _f:
    _bimap = {int(v['GEANTID']):int(v['PDGID']) for v in csv.DictReader(_f)}


class GeantID(int):
    """
    Holds a Geant ID.

    Examples
    --------
    >>> geantid = GeantID(8)

    >>> from particle import Particle
    >>> p = Particle.from_pdgid(geantid.to_pdgid())

    >>> p = Particle.find(pdgid=geantid.to_pdgid())
    >>> p.name
    'pi+'
    """

    __slots__ = ()  # Keep PythiaID a slots based class

    @classmethod
    def from_pdgid(cls, pdgid):
        """
        Constructor from a PDGID.
        """
        for k, v in _bimap.items():
            if v == pdgid:
                return cls(k)
        raise MatchingIDNotFound("Non-existent GeantID for input PDGID {0} !".format(pdgid))

    def to_pdgid(self):
        return PDGID(_bimap[self])

    def __repr__(self):
        return "<GeantID: {:d}>".format(int(self))

    def __str__(self):
        return repr(self)

    def __neg__(self):
        """
        Note:
        Allowed operation though ALL Geant identification codes are positive!
        """
        return self.__class__(-int(self))

    __invert__ = __neg__
