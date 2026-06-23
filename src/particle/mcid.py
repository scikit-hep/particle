# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Base class for particle identification codes used by Monte Carlo programs.
"""

from __future__ import annotations

import csv
from collections.abc import Mapping
from typing import ClassVar, TypeVar

from . import data
from .exceptions import MatchingIDNotFound
from .pdgid import PDGID

Self = TypeVar("Self", bound="MCParticleID")


def _csv_to_pdg_map(filename: str, id_column: str) -> dict[int, int]:
    """
    Read an <ID> -> PDG ID conversion table from a CSV file
    shipped in the package data.

    Examples of <ID>: Corsika7ID, Geant3ID, PythiaID.
    """
    with data.basepath.joinpath(filename).open() as f:
        return {
            int(row[id_column]): int(row["PDGID"])
            for row in csv.DictReader(line for line in f if not line.startswith("#"))
        }


# Per-class caches of the inverse (PDG ID -> ID) conversion maps,
# each built once on first use.
_from_pdg_maps: dict[type, dict[int, int]] = {}


class MCParticleID(int):
    """
    Base class for particle identification codes ("IDs") used by
    Monte Carlo programs, convertible to and from the standard PDG IDs.

    Concrete ID classes derive from this class and either

    - Define a class-level `_to_pdg_map` mapping of their IDs to PDG IDs,
      in which case `to_pdgid` and `from_pdgid` are provided automatically, or
    - Override `to_pdgid` and `from_pdgid`, e.g. when the conversion
      is algorithmic and no explicit mapping is needed.

    Examples
    --------
    Define a custom ID class `MyGeneratorID` given a known mapping to PDG IDs:

    >>> class MyGeneratorID(MCParticleID):
    ...     _to_pdg_map = {1: 11, 2: -11, 3: 22}
    >>> MyGeneratorID(3).to_pdgid()
    <PDGID: 22>
    >>> MyGeneratorID.from_pdgid(PDGID(-11))
    <MyGeneratorID: 2>
    """

    __slots__ = ()  # Keep MCParticleID a slots based class

    _to_pdg_map: ClassVar[Mapping[int, int]]

    @classmethod
    def _conversion_map(cls) -> Mapping[int, int]:
        try:
            return cls._to_pdg_map
        except AttributeError:
            msg = (
                f"{cls.__name__} should either define a '_to_pdg_map' mapping "
                "or override 'to_pdgid' and 'from_pdgid'."
            )
            raise NotImplementedError(msg) from None

    @classmethod
    def _inverse_conversion_map(cls) -> Mapping[int, int]:
        if cls not in _from_pdg_maps:
            _from_pdg_maps[cls] = {
                pdgid: mcid for mcid, pdgid in cls._conversion_map().items()
            }
        return _from_pdg_maps[cls]

    def to_pdgid(self) -> PDGID:
        """
        Convert to the matching PDGID.

        Raises
        ------
        MatchingIDNotFound
            If no matching PDGID exists.
        """
        try:
            return PDGID(self._conversion_map()[int(self)])
        except KeyError:
            raise MatchingIDNotFound(
                f"Non-existent PDGID for input {self.__class__.__name__} {int(self)}!"
            ) from None

    @classmethod
    def from_pdgid(cls: type[Self], pdgid: int) -> Self:
        """
        Constructor from a PDGID.

        Raises
        ------
        MatchingIDNotFound
            If no matching ID exists.
        """
        try:
            return cls(cls._inverse_conversion_map()[int(pdgid)])
        except KeyError:
            raise MatchingIDNotFound(
                f"Non-existent {cls.__name__} for input PDGID {pdgid}!"
            ) from None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {int(self):d}>"

    def __str__(self) -> str:
        return repr(self)
