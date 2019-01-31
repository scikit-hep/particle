# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Functions relevant to particle kinematics.
"""

from __future__ import absolute_import, division, print_function

from hepunits.units import MeV, ns
from hepunits.constants import hbar



def width_to_lifetime(Gamma):
    """
    Convert from a particle decay width to a lifetime.

    Parameters
    ----------
    Gamma : float > 0
        Particle decay width, typically in MeV (any HEP energy unit is OK).

    Returns
    -------
    Particle lifetime, in the HEP standard time unit ns.
    """

    if Gamma <= 0.:
        raise ValueError( 'Input provided, %s <= 0!'.format(Gamma) )

    # Just need to first make sure that the width is in the standard unit MeV
    return hbar / float(Gamma / MeV)


def lifetime_to_width(tau):
    """
    Convert from a particle lifetime to a decay width.

    Parameters
    -----------
    tau : float > 0
        Particle lifetime, typically in picoseconds (any HEP time unit is OK).

    Returns
    -------
    Particle decay width, in the HEP standard energy unit MeV.
    """

    if tau <= 0:
        raise ValueError( 'Input provided, %s <= 0!'.format(tau) )

    # Just need to first make sure that the lifetime is in the standard unit ns
    return hbar / float(tau / ns)
