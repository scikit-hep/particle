# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from typing import Tuple

from .enums import Charge, Inv, Parity, SpinType, Status
from .kinematics import lifetime_to_width, width_to_lifetime
from .particle import InvalidParticle, Particle, ParticleNotFound
from .utilities import latex_name_unicode, latex_to_html_name, programmatic_name

__all__ = (
    "Charge",
    "Inv",
    "Parity",
    "SpinType",
    "Status",
    "lifetime_to_width",
    "width_to_lifetime",
    "InvalidParticle",
    "Particle",
    "ParticleNotFound",
    "latex_name_unicode",
    "latex_to_html_name",
    "programmatic_name",
)


def __dir__():
    # type: () -> Tuple[str, ...]
    return __all__
