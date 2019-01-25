# -*- encoding: utf-8 -*-
"""
Definitions of handy particle literals
======================================

The particle literals provide aliases for most common particles, with easily recognisable names.
The aliases are instances of the Particle class.

Typical use cases::

    >>> from particle.particle import literals as lp
    >>> lp.pi_plus
    <Particle: pdgid=211, fullname='pi+', mass=139.57061 ± 0.00024 MeV>
    >>> lp.pi_plus.is_meson
    1.0
    >>> from particle.particle.literals import Lb0
    >>>> Lb0
    <Particle: pdgid=5122, fullname='Lambda(b)0', mass=5619.60 ± 0.17 MeV>
    >>> Lb0.J
    0.5

List of available/defined particle literals:

{0}
"""
from ..shared_literals import common_particles
from .particle import Particle, ParticleNotFound

for item in common_particles:
    try:
        locals()[item] = Particle.from_pdgid(common_particles[item])
    except ParticleNotFound:
        pass


__doc = ""
for item in common_particles: __doc += "  {item!s} = Particle.from_pdgid({part})\n".format(item=item, part=common_particles[item])

__doc__ = __doc__.format(__doc)


del Particle, ParticleNotFound, common_particles
