# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import absolute_import

# Convenient access to the version number
from .version import __version__

# Direct access to PDGID
from .pdgid import PDGID

# Direct access to Particle (the CSV file is not read until a particle is accessed)
from .particle import Particle, SpinType, Parity, Charge, Inv, Status
