# Licensed under a 3-clause BSD style license, see LICENSE.

import pytest
from pytest import approx

from particle.particle import width_to_lifetime
from particle.particle import lifetime_to_width

from hepunits.units import MeV, GeV, ps
from hepunits.constants import hbar


def test_valid_width_lifetime_conversions():
    assert lifetime_to_width(1.5*ps)/GeV == approx(4.388079676311604e-13)
    assert 1.5*ps * lifetime_to_width(1.5*ps) == hbar
    assert width_to_lifetime(hbar) == 1 * MeV


def test_invalid_width_lifetime_conversions():
    with pytest.raises(ValueError):
        lifetime_to_width(-1)
    with pytest.raises(ValueError):
        width_to_lifetime(-1)

    assert lifetime_to_width(0) == float('inf')
    assert width_to_lifetime(0) == float('inf')
