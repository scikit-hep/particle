# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Helper (internal) module with particle aliases
for all particles in the loaded "database" CSV file, excluding nuclei.

See the particle.literals and the pdgid.literals submodules for the actually exposed aliases.
"""


from __future__ import annotations

from .particle import Particle

# Make aliases for all particles in the latest "database", excluding nuclei
common_particles = {
    p.programmatic_name: int(p.pdgid)
    for p in Particle.findall(lambda p: abs(p.pdgid) < 1000000000)
}

# Some extra names that are expected:
common_particles.update(
    photon=22,  # official programmatic name is "gamma"
    Higgs=25,  # official programmatic name is "H_0"
    proton=2212,  # official programmatic name is "p"
    antiproton=-2212,  # official programmatic name is "p_bar"
    neutron=2112,  # official programmatic name is "n"
    antineutron=-2112,  # official programmatic name is "n_bar"
)
