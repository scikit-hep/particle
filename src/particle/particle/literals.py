# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
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

from __future__ import annotations

from ..shared_literals import common_particles
from .particle import Particle


def __dir__() -> list[str]:
    return list(common_particles)


for item in common_particles:
    locals()[item] = Particle.from_pdgid(common_particles[item])


__doc = "".join(
    f"  {item} = Particle.from_pdgid({common_particles[item]})\n"
    for item in common_particles
)
__doc__ = __doc__.format(__doc)
