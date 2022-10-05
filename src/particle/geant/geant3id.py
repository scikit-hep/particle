# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Class representing a Geant3 ID.

Note
----
No equivalent Geant4 ID class is available/necessary given that Geant4
follows the PDG rules, hence uses the standard PDG IDs.
"""


from __future__ import annotations

import csv
from typing import TypeVar

from .. import data
from ..exceptions import MatchingIDNotFound
from ..pdgid import PDGID

Self = TypeVar("Self", bound="Geant3ID")


with data.basepath.joinpath("pdgid_to_geant3id.csv").open() as _f:
    _bimap = {
        int(v["GEANT3ID"]): int(v["PDGID"])
        for v in csv.DictReader(line for line in _f if not line.startswith("#"))
    }


class Geant3ID(int):
    """
    Holds a Geant3 ID.

    Examples
    --------
    >>> gid = Geant3ID(8)

    >>> from particle import Particle
    >>> p = Particle.from_pdgid(gid.to_pdgid())

    >>> (p,) = Particle.finditer(pdgid=gid.to_pdgid())
    >>> p.name
    'pi+'
    """

    __slots__ = ()  # Keep PythiaID a slots based class

    @classmethod
    def from_pdgid(cls: type[Self], pdgid: int) -> Self:
        """
        Constructor from a PDGID.
        """
        for k, v in _bimap.items():
            if v == pdgid:
                return cls(k)
        raise MatchingIDNotFound(f"Non-existent Geant3ID for input PDGID {pdgid} !")

    def to_pdgid(self) -> PDGID:
        return PDGID(_bimap[self])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {int(self):d}>"

    def __str__(self) -> str:
        return repr(self)

    def __neg__(self: Self) -> Self:
        """
        Note:
        Allowed operation though ALL Geant3 identification codes are positive!
        """
        return self.__class__(-int(self))

    __invert__ = __neg__
