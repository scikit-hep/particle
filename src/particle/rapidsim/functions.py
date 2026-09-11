# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

from ..particle import Particle
from .converters import RapidSimName2PDGIDBiMap


def to_rapidsim_name(p: Particle) -> str:
    """
    Convert a :class:`Particle` to the name used in RapidSim.

    Raises
    ------
    MatchingIDNotFound
        If no RapidSim name exists for the given particle.

    Examples
    --------
    >>> p = Particle.from_pdgid(531)
    >>> to_rapidsim_name(p)
    'Bs0'
    """
    return RapidSimName2PDGIDBiMap[p.pdgid]


def from_rapidsim_name(name: str) -> Particle:
    """
    Get a :class:`Particle` from a RapidSim particle name.

    Raises
    ------
    ParticleNotFound
        If :meth:`Particle.from_pdgid` returns no match.
    MatchingIDNotFound
        If the RapidSim name has no corresponding PDG ID entry.

    Examples
    --------
    >>> from_rapidsim_name('Bs0')
    <Particle: name="B(s)0", pdgid=531, mass=5366.93 ± 0.10 MeV>
    """
    return Particle.from_pdgid(RapidSimName2PDGIDBiMap[name])
