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

# Some Corsika7 ID's are not really particles
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

    All arithmetic operations on the class (like `-Corsika7ID(5)`) will
    return an integer. This is unlike for example `-PDGID(13)`, which will
    return `PDGID(-13)`. But since negative values have no direct meaning
    as a Corsika7ID, (in the output file they are used to indicate mother-particles)
    we omit this feature.

    Examples
    --------
    >>> cid = Corsika7ID(6)

    >>> from particle import Particle
    >>> p = Particle.from_pdgid(cid.to_pdgid())

    >>> (p,) = Particle.finditer(pdgid=cid.to_pdgid())
    >>> p.name
    'mu-'
    """

    __slots__ = ()  # Keep Corsika7ID a slots based class

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
        bool:       If the particle is a (grand)mother particle.
        """
        cid = abs(particle_description) // 1000
        ismother = particle_description < 0

        if cls._is_non_particle_id(cid):
            return cls(cid), ismother

        # This catches the cases of nuclei with no known PDG ID
        if 200 <= cid < 5699:
            return cls(cid), ismother

        if cid in _bimap:
            return cls(cid), ismother

        raise MatchingIDNotFound(
            f"Non-existent Corsika7ID for particle description {particle_description}!"
        )

    @classmethod
    def _is_non_particle_id(cls: type[Self], corsikaid: int) -> bool:
        """
        Returns True if the ID is valid but does not correspond to a particle, False otherwise.
        """
        return (
            corsikaid in _non_particles
            or corsikaid // 1000 == 8888
            or corsikaid == 9900
        )

    def is_particle(self) -> bool:
        """
        Returns True if the ID really belongs to a particle, since some are for example additional information.

        Examples
        --------
        >>> mu_minux = Corsika7ID(6)
        >>> mu_minus.is_particle()
        True
        >>> mu_info = Corsika7ID(76)
        >>> mu_info.is_particle()
        False
        >>> mu_info.name()
        'μ− add. info.'
        """
        iid = int(self)

        return not self._is_non_particle_id(iid)

    def name(self) -> str:
        """
        Returns a human readable name of the Corsika7ID.
        This also works for non-particles (is_particle()==false).

        Raises
        ------
        ParticleNotFound
            If it is a 'valid' PDG particle, but unknown.
            This for example happens with strange nuclei, which are not in the nuclei list.

        Examples
        --------
        >>> mu_minus = Corsika7ID(6)
        >>> mu_minus.is_particle()
        True
        >>> mu_minus.name() # For a particle, this returns the same name as `Particle.name`
        'mu'
        >>> mu_info = Corsika7ID(76)
        >>> mu_info.is_particle()
        False
        >>> mu_info.name()
        'μ− add. info.'
        >>> ch_photons_of = Corsika7ID(9900)
        >>> ch_photons_of.is_particle()
        False
        >>> ch_photons_of.name()
        'Cherenkov photons on particle output file'
        """
        from ..particle.particle import Particle  # pylint: disable=C0415

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
            If it is a valid Corsika particle, but not a valid PDGID.

        Examples
        --------
        >>> Corsika7ID(6).to_pdgid()
        <PDGID: 13>
        >>> Corsika7ID(76).to_pdgid()
        InvalidParticle: The Corsika7ID <Corsika7ID: 76> does not correspond to a particle and thus has no equivalent PDGID.
        """
        from ..particle.particle import InvalidParticle  # pylint: disable=C0415

        if self not in _bimap:
            raise InvalidParticle(
                f"The Corsika7ID {self} does not correspond to a particle and thus has no equivalent PDGID."
            )
        return PDGID(_bimap[self])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {int(self):d}>"

    def __str__(self) -> str:
        return repr(self)
