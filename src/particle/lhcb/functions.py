# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

from ..particle import Particle
from .converters import LHCbName2PDGIDBiMap


def to_lhcb_name(p: Particle) -> str:
    """
    Convert to the name used in the LHCb software framework.

    Examples
    --------
    >>> p = Particle.from_pdgid(-531)
    >>> p
    <Particle: name="B(s)~0", pdgid=-531, mass=5366.88 ± 0.14 MeV>
    >>> to_lhcb_name(p)
    'B_s~0'
    """
    return LHCbName2PDGIDBiMap[p.pdgid]


def from_lhcb_name(name: str) -> Particle:
    """
    Get a `Particle` from an LHCb particle name, as used in LHCb Gaudi applications.

    Examples
    --------
    >>> from_lhcb_name("B_s~0")
    <Particle: name="B(s)~0", pdgid=-531, mass=5366.88 ± 0.14 MeV>

    Raises
    ------
    ParticleNotFound
        If `from_pdgid` returns no match.
    MatchingIDNotFound
        If the matching LHCb name - PDG ID done internally is unsuccessful.
    """
    return Particle.from_pdgid(LHCbName2PDGIDBiMap[name])
