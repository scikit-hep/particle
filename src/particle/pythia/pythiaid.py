# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Class representing a Pythia ID.
"""


from __future__ import annotations

import csv
from typing import TypeVar

from .. import data
from ..exceptions import MatchingIDNotFound
from ..pdgid import PDGID

with data.basepath.joinpath("pdgid_to_pythiaid.csv").open() as _f:
    _bimap = {
        int(v["PYTHIAID"]): int(v["PDGID"])
        for v in csv.DictReader(line for line in _f if not line.startswith("#"))
    }


Self = TypeVar("Self", bound="PythiaID")


class PythiaID(int):
    """
    Holds a Pythia ID.

    Examples
    --------
    >>> pythiaid = PythiaID(211)

    >>> from particle import Particle
    >>> p = Particle.from_pdgid(pythiaid.to_pdgid())

    >>> (p,) = Particle.finditer(pdgid=pythiaid.to_pdgid())
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
        raise MatchingIDNotFound(f"Non-existent PythiaID for input PDGID {pdgid} !")

    def to_pdgid(self) -> PDGID:
        return PDGID(_bimap[self])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {int(self):d}>"

    def __str__(self) -> str:
        return repr(self)

    def __neg__(self: Self) -> Self:
        return self.__class__(-int(self))

    __invert__ = __neg__
