# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Definitions of handy particle `Particle` literals
=================================================

The particle literals provide aliases for most common particles, with easily recognisable names.
The aliases are instances of the Particle class.

Typical use cases::

    >>> from particle import literals as lp
    >>> lp.pi_plus
    <Particle: name="pi+", pdgid=211, mass=139.57039 ± 0.00018 MeV>
    >>> lp.pi_plus.name
    'pi+'
    >>> from particle.literals import Lambda_b_0
    >>> Lambda_b_0
    <Particle: name="Lambda(b)0", pdgid=5122, mass=5619.60 ± 0.17 MeV>
    >>> Lambda_b_0.J
    0.5

List of available/defined literals:

{0}
"""

from ..shared_literals import common_particles
from .particle import Particle, ParticleNotFound

for item in common_particles:
    locals()[item] = Particle.from_pdgid(common_particles[item])


__doc = "".join(
    "  {item!s} = Particle.from_pdgid({pdgid})\n".format(
        item=item, pdgid=common_particles[item]
    )
    for item in common_particles
)
__doc__ = __doc__.format(__doc)


del Particle, ParticleNotFound, common_particles, item
