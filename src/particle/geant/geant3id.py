# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
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

from typing import TypeVar

from ..mcid import MCParticleID, _csv_to_pdg_map

Self = TypeVar("Self", bound="Geant3ID")


class Geant3ID(MCParticleID):
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

    __slots__ = ()  # Keep Geant3ID a slots based class

    _to_pdg_map = _csv_to_pdg_map("pdgid_to_geant3id.csv", "GEANT3ID")

    def __neg__(self: Self) -> Self:
        """
        Note:
        Allowed operation though ALL Geant3 identification codes are positive!
        """
        return self.__class__(-int(self))

    __invert__ = __neg__
