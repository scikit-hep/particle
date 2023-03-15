# Copyright (c) 2018-2023, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest
from hepunits.constants import hbar
from hepunits.units import GeV, MeV, ps
from pytest import approx

from particle.particle import lifetime_to_width, width_to_lifetime


def test_valid_width_lifetime_conversions():
    assert lifetime_to_width(1.5 * ps) / GeV == approx(4.388079676311604e-13)
    assert 1.5 * ps * lifetime_to_width(1.5 * ps) == hbar
    assert width_to_lifetime(hbar) == 1 * MeV


def test_invalid_width_lifetime_conversions():
    with pytest.raises(ValueError, match="Input provided, -1 <= 0!"):
        lifetime_to_width(-1)
    with pytest.raises(ValueError, match="Input provided, -1 <= 0!"):
        width_to_lifetime(-1)

    assert lifetime_to_width(0) == float("inf")
    assert width_to_lifetime(0) == float("inf")
