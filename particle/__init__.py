# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

# Convenient access to the version number
from ._version import __version__

# Direct access to PDGID
from .pdgid import PDGID

# Direct access to Particle (the CSV file is not read until a particle is accessed)
from .particle import Particle, SpinType, Parity, Charge, Inv, Status, ParticleNotFound

# Direct access to kinematics functions
from .particle import width_to_lifetime, lifetime_to_width

# Direct access to handy LaTeX to HTML particle name conversions
from .particle import latex_to_html_name
