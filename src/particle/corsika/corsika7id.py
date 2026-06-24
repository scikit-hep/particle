# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
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

from typing import TypeVar

from ..exceptions import MatchingIDNotFound
from ..mcid import MCParticleID, _csv_to_pdg_map
from ..particle.particle import InvalidParticle, Particle
from ..pdgid import PDGID

Self = TypeVar("Self", bound="Corsika7ID")


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


class Corsika7ID(MCParticleID):
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

    _to_pdg_map = _csv_to_pdg_map("pdgid_to_corsika7id.csv", "CORSIKA7ID")

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

        # These are all nuclei allowed by CORSIKA7,
        # Reference: Page 130 of the CORSIKA7 userguide Version 7.8050
        # https://www.iap.kit.edu/corsika/downloads/CORSIKA_GUIDE7.8050.pdf
        # Note: Particles with A>Z do not make sense
        # But in principle the CORSIKA7 numbering scheme allows them
        if 200 <= cid <= 5699:
            return cls(cid), ismother

        if cid in cls._to_pdg_map:
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
        >>> mu_minus = Corsika7ID(6)
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

        InvalidParticle
            If the Corsika7ID itself is not valid.

        Examples
        --------
        >>> mu_minus = Corsika7ID(6)
        >>> mu_minus.is_particle()
        True
        >>> mu_minus.name() # For a particle, this returns the same name as `Particle.name`
        'mu-'
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
        if not self.is_particle():
            iid = int(self)

            if iid in _non_particles:
                return _non_particles[iid]

            if iid // 1000 == 8888:
                return "weights of preceding particle (MULTITHIN option)"

            if iid == 9900:
                return "Cherenkov photons on particle output file"

        return str(Particle.from_pdgid(self.to_pdgid()).name)

    def to_pdgid(self) -> PDGID:
        """
        Convert to the matching PDGID.

        Raises
        ------
        InvalidParticle
            If the Corsika7ID does not correspond to a particle, either
            because it holds additional information (`is_particle()` is False)
            or because it is no valid Corsika7ID at all.

        MatchingIDNotFound
            If the Corsika7ID is a particle but has no matching PDGID,
            i.e. nuclei unknown to the PDG.

        Examples
        --------
        >>> Corsika7ID(6).to_pdgid()
        <PDGID: 13>
        >>> Corsika7ID(76).to_pdgid()  # doctest: +SKIP
        InvalidParticle: The Corsika7ID <Corsika7ID: 76> does not correspond to a particle and thus has no equivalent PDGID.
        """
        if int(self) in self._to_pdg_map:
            return super().to_pdgid()

        # Some nuclei with no known PDG ID are valid C7 IDs nonetheless.
        # Particles with existing PDGIDs are in the csv conversion file
        # and are caught by the first `if`.
        # Reference: Page 130 of the CORSIKA7 userguide Version 7.8050
        # https://www.iap.kit.edu/corsika/downloads/CORSIKA_GUIDE7.8050.pdf.
        if self.is_particle() and 200 <= int(self) <= 5699:
            raise MatchingIDNotFound(
                f"Non-existent PDGID for input {self.__class__.__name__} {int(self)}!"
            )

        raise InvalidParticle(
            f"The Corsika7ID {self} does not correspond to a particle and thus has no equivalent PDGID."
        )
