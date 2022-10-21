# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Class representing a Corsika7 ID.

Note
----
Corsika8 uses Geant3 Particle IDs.
"""


from __future__ import annotations

import csv
from typing import TypeVar

from .. import data
from ..exceptions import MatchingIDNotFound
from ..pdgid import PDGID

Self = TypeVar("Self", bound="Corsika7ID")


with data.basepath.joinpath("pdgid_to_corsika7id.csv").open() as _f:
    _bimap = {
        int(v["CORSIKA7ID"]): int(v["PDGID"])
        for v in csv.DictReader(line for line in _f if not line.startswith("#"))
    }

# Some Corsika ID's are not really particles
_non_particles = {
    71: "η → γγ",
    72: "η → 3π◦",
    73: "η → π+π−π◦",
    74: "η → π+π−γ",
    75: "μ+ add. info.",
    76: "μ− add. info.",
    85: "decaying μ+ at start",
    86: "decaying μ− at start",
    95: "decaying μ+ at end",
    96: "decaying μ− at end",
}


class Corsika7ID(int):
    """
    Holds a Corsika7 ID.

    Examples
    --------
    >>> cid = Corsika7ID(6)

    >>> from particle import Particle
    >>> p = Particle.from_pdgid(cid.to_pdgid())

    >>> (p,) = Particle.finditer(pdgid=cid.to_pdgid())
    >>> p.name
    'mu-'
    """

    @classmethod
    def from_pdgid(cls: type[Self], pdgid: int) -> Self:
        """
        Constructor from a PDGID.
        """
        for k, v in _bimap.items():
            if v == pdgid:
                return cls(k)
        raise MatchingIDNotFound(f"Non-existent Corsika7ID for input PDGID {pdgid}!")

    @classmethod
    def from_particle_description(
        cls: type[Self], particle_description: int
    ) -> tuple[Self, bool]:
        """
        Constructor from the particle description returned by Corsika7
        in the particle data sub-block, mother particle data sub-block or
        the grandmother particle data sub-block.

        Returns
        -------
        A tuple with
        
        Corsika7ID: The Corsika7 id
        bool:       If the particle is a (grand)motherparticle.
        """
        cid = abs(particle_description) // 1000
        ismother = particle_description < 0

        if cls._is_non_particle_id(cid):
            return cls(cid), ismother

        # this catches the case, of nuclei with no known PDGid
        if cid >= 200 and cid < 5699:
            return cls(cid), ismother

        if cid in _bimap:
            return cls(cid), ismother

        raise MatchingIDNotFound(
            f"Non-existent Corsika7ID for particle description {particle_description}!"
        )

    @classmethod
    def _is_non_particle_id(cls: type[Self], id: int) -> bool:
        """
        returns True if the id is a valid id, but not a particle, False otherwise.
        """
        return id in _non_particles or id // 1000 == 8888 or id == 9900

    def is_particle(self) -> bool:
        """
        Returns if the corsikaid really belongs to a particle, since some are for example additional information.
        """
        iid = int(self)

        return not self._is_non_particle_id(iid)

    def name(self) -> str:
        """
        Returns a human readable name of the Corsika ID.
        This also works for non-particles (is_particle()==false).

        Raises
        ------
        ParticleNotFound
            If it is a 'valid' PDG particle, but unknown.
            This for example happens with strange nuclei, which are not in the nuclei list.
        """
        from ..particle.particle import Particle

        if self.is_particle():
            return str(Particle.from_pdgid(self.to_pdgid()).name)

        iid = int(self)

        if iid in _non_particles:
            return _non_particles[iid]

        if iid // 1000 == 8888:
            return "weights of preceding particle (MULTITHIN option)"

        if iid == 9900:
            return "Cherenkov photons on particle output file"

        raise RuntimeError("This should be unreachable.")

    def to_pdgid(self) -> PDGID:
        """
        Raises
        ------
        InvalidParticle
            If it is a valid Corsika particle, but not a valid PDGid particle.
        """
        from ..particle.particle import InvalidParticle

        if self not in _bimap:
            raise InvalidParticle(
                f"The Corsika7Id {self} is not a valid PDGID particle."
            )
        return PDGID(_bimap[self])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {int(self):d}>"

    def __str__(self) -> str:
        return repr(self)
