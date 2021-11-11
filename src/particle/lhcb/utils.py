# -*- coding: utf-8 -*-

from ..particle import Particle
from .converters.lhcb import LHCbName2PDGIDBiMap


def to_lhcb_name(p):
    # type: (Particle) -> str
    "Convert to the name used in the LHCb software framework"
    return LHCbName2PDGIDBiMap[p.pdgid]


def from_lhcb_name(name):
    # type: (str) -> Particle
    """
    Get a particle from an LHCb particle name, as used in LHCb Gaudi applications
    Raises
    ------
    ParticleNotFound
        If `from_pdgid` returns no match.
    MatchingIDNotFound
        If the matching LHCb name - PDG ID done internally is unsuccessful.
    """
    return Particle.from_pdgid(LHCbName2PDGIDBiMap[name])
