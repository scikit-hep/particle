# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Class representing a Pythia ID.
"""

from __future__ import annotations

from typing import TypeVar

from ..mcid import MCParticleID
from ..pdgid import PDGID

Self = TypeVar("Self", bound="PythiaID")

# Pythia follows the standard PDG particle numbering scheme, except for a
# few light scalar mesons, for which it kept older PDG numberings.
_pdgid_to_pythiaid = {
    10221: 10331,  # f(0)(1370)
    9000111: 10111,  # a(0)(980)0
    9000211: 10211,  # a(0)(980)+
    -9000211: -10211,  # a(0)(980)-
    9010221: 10221,  # f(0)(980)
}
_pythiaid_to_pdgid = {v: k for k, v in _pdgid_to_pythiaid.items()}


class PythiaID(MCParticleID):
    """
    Holds a Pythia ID.

    Pythia IDs are identical to PDG IDs apart from a few legacy numberings
    of light scalar mesons, hence conversions are done algorithmically
    rather than via an explicit conversion table.

    Examples
    --------
    >>> pythiaid = PythiaID(211)

    >>> from particle import Particle
    >>> p = Particle.from_pdgid(pythiaid.to_pdgid())

    >>> (p,) = Particle.finditer(pdgid=pythiaid.to_pdgid())
    >>> p.name
    'pi+'

    >>> PythiaID(10221).to_pdgid()
    <PDGID: 9010221>
    """

    __slots__ = ()  # Keep PythiaID a slots based class

    def to_pdgid(self) -> PDGID:
        """
        Convert to the matching PDGID.
        """
        return PDGID(_pythiaid_to_pdgid.get(int(self), int(self)))

    @classmethod
    def from_pdgid(cls: type[Self], pdgid: int) -> Self:
        """
        Constructor from a PDGID.
        """
        return cls(_pdgid_to_pythiaid.get(int(pdgid), int(pdgid)))

    def __neg__(self: Self) -> Self:
        return self.__class__(-int(self))

    __invert__ = __neg__
