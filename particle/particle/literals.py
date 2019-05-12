# -*- encoding: utf-8 -*-
# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Definitions of handy particle literals
======================================

The particle literals provide aliases for most common particles, with easily recognisable names.
The aliases are instances of the Particle class.

Typical use cases::

    >>> from particle.particle import literals as lp
    >>> lp.pi_plus
    <Particle: name="pi+", pdgid=211, mass=139.57061 ± 0.00024 MeV>
    >>> lp.pi_plus.name
    'pi+'
    >>> from particle.particle.literals import Lambda_b_0
    >>> Lambda_b_0
    <Particle: name="Lambda(b)0", pdgid=5122, mass=5619.60 ± 0.17 MeV>
    >>> Lambda_b_0.J
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
