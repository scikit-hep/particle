# -*- coding: utf-8 -*-
from ..particle import Particle as BaseParticle
from .converters.lhcb import LHCbName2PDGIDBiMap


class Particle(BaseParticle):
    def __str__(self):
        # type: () -> str
        return self.lhcb_name

    @property
    def lhcb_name(self):
        # type: () -> str
        "This is the name used in the LHCb software framework"
        return LHCbName2PDGIDBiMap[self.pdgid]

    @classmethod
    def from_lhcb_name(cls, name):
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
        return cls.from_pdgid(LHCbName2PDGIDBiMap[name])
