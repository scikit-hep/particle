# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Functions relevant to particle kinematics.
"""


from __future__ import annotations

from hepunits.constants import hbar
from hepunits.units import MeV, ns


def width_to_lifetime(Gamma: float) -> float:
    """
    Convert from a particle decay width to a lifetime.

    Parameters
    ----------
    Gamma : float > 0
        Particle decay width, in the HEP standard energy unit MeV.

    Returns
    -------
    Gamma > 0: particle lifetime, in the HEP standard time unit ns.
    Gamma = 0: Infinity (float("inf")).
    Gamma < 0: an exception ValueError is raised.

    Examples
    --------
    Manipulation with no explicit usage of units:

    >>> width_to_lifetime(4.33e-10)   # result returned in ns
    0.0015201199929582136

    Manipulations with explicit units defined in the HEP system of units:

    >>> from hepunits.units import MeV, eV, ps   # handy module with units in the HEP system of units
    >>>
    >>> width_to_lifetime(4.33e-10*MeV)   # result returned in ns
    0.0015201199929582136
    >>>
    >>> width_to_lifetime(4.33e-4*eV)   # result again returned in ns
    0.0015201199929582136
    >>>
    >>> width_to_lifetime(4.33e-10*MeV)/ps   # result converted to ps
    1.5201199929582137
    """

    if Gamma < 0.0:
        raise ValueError(f"Input provided, {Gamma} <= 0!")
    if Gamma == 0:
        return float("inf")

    # Just need to first make sure that the width is in the standard unit MeV
    return hbar / float(Gamma / MeV)


def lifetime_to_width(tau: float) -> float:
    """
    Convert from a particle lifetime to a decay width.

    Parameters
    -----------
    tau : float > 0
        Particle lifetime, in the HEP standard time unit ns.

    Returns
    -------
    Particle decay width, in the HEP standard energy unit MeV.
    tau > 0: particle lifetime, in the HEP standard time unit ns.
    tau = 0: Infinity (float("inf")).
    tau < 0: an exception ValueError is raised.

    Examples
    --------
    Manipulation with no explicit usage of units:

    >>> lifetime_to_width(0.0015201199929582136)   # result returned in MeV
    4.33e-10

    Manipulations with explicit units defined in the HEP system of units:

    >>> from hepunits.units import MeV, eV, ps   # handy module with units in the HEP system of units
    >>>
    >>> lifetime_to_width(0.0015201199929582136*ns)   # result returned in MeV
    4.33e-10
    >>>
    >>> lifetime_to_width(1.5201199929582137*ps)   # result again returned in MeV
    4.33e-10
    >>>
    >>> lifetime_to_width(1.5201199929582137*ps)/eV   # result converted to eV
    0.000433
    """

    if tau < 0:
        raise ValueError(f"Input provided, {tau} <= 0!")
    if tau == 0:
        return float("inf")

    # Just need to first make sure that the lifetime is in the standard unit ns
    return hbar / float(tau / ns)
