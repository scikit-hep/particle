# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest
import sys

from particle import Particle
from particle.particle.utilities import programmatic_name
from particle.particle.utilities import str_with_unc
from particle.particle.particle import ParticleNotFound


possibilites = (
    (1.234567, 0.01, None, u"1.235 ± 0.010"),
    (1.234567e-9, 0.01e-9, None, u"1.235e-09 ± 1.0e-11"),
    (1.234567e9, 0.04e9, None, u"1.23e+09 ± 4e+07"),
    (0.001, 0.00001, None, u"1.000e-03 ± 1.0e-05"),
    (0.00099, 0.00001, None, u"9.90e-04 ± 1.0e-05"),
    (99, 0.24, None, u"99.00 ± 0.24"),
    (100, 0.25, None, u"100.0 ± 0.2"),
    (101, 0.26, None, u"101.0 ± 0.3"),
    (0.00001231, 0.000002, 0.000004, u"1.23e-05 + 2.0e-06 - 4.0e-06"),
    (1234.5, 0.03, 0.03, u"1234.50 ± 0.03"),
    (1234.5, 5, 5, u"1234 ± 5"),
    (1234.5, 2, 2, u"1234.5 ± 2.0"),
)


@pytest.mark.parametrize("value,err_u,err_l,test_str", possibilites)
def test_unc_printout(value, err_u, err_l, test_str):

    if sys.version_info < (3, 0):
        test_str = test_str.replace(u"±", u"+/-")

    assert str_with_unc(value, err_u, err_l) == test_str
