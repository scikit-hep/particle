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
from ..particle import Particle
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

    def is_particle(self) -> bool:
        """
        Returns if the corsikaid really belongs to a particle, since some are for example additional information.
        """
        iid = int(self)

        return not (iid in _non_particles or iid // 1000 == 8888 or iid == 9900)

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
        return PDGID(_bimap[self])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {int(self):d}>"

    def __str__(self) -> str:
        return repr(self)
