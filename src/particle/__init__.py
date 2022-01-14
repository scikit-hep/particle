# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


import sys
from typing import Tuple

# Direct access to other ID classes
from .geant import Geant3ID

# Direct access to Particle literals
# Direct access to Particle (the CSV file is not read until a particle is accessed)
from .particle import InvalidParticle, Particle, ParticleNotFound, literals
from .particle.enums import Charge, Inv, Parity, SpinType, Status

# Direct access to PDGID and other ID classes
from .pdgid import PDGID
from .pythia import PythiaID

# Convenient access to the version number
from .version import version as __version__

sys.modules["particle.literals"] = literals

# Direct access to handy LaTeX to HTML particle name conversions
# Direct access to kinematics functions
from .particle import latex_to_html_name, lifetime_to_width, width_to_lifetime

__all__ = (
    "Charge",
    "Geant3ID",
    "Inv",
    "InvalidParticle",
    "PDGID",
    "Parity",
    "Particle",
    "ParticleNotFound",
    "PythiaID",
    "SpinType",
    "Status",
    "latex_to_html_name",
    "lifetime_to_width",
    "width_to_lifetime",
    "__version__",
)


def __dir__() -> Tuple[str, ...]:
    return __all__
