# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import sys

# Convenient access to the version number
from .version import version as __version__

# Direct access to PDGID
from .pdgid import PDGID

# Direct access to other ID classes
from .geant import Geant3ID
from .pythia import PythiaID

# Direct access to Particle (the CSV file is not read until a particle is accessed)
from .particle import Particle, SpinType, Parity, Charge, Inv, Status
from .particle import ParticleNotFound, InvalidParticle

# Direct access to Particle literals
from .particle import literals

sys.modules["particle.literals"] = literals

# Direct access to kinematics functions
from .particle import width_to_lifetime, lifetime_to_width

# Direct access to handy LaTeX to HTML particle name conversions
from .particle import latex_to_html_name

# Direct access to handy bi-directional maps
from .converters import Pythia2PDGIDBiMap
