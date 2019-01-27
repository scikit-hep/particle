# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license, see LICENSE.

import pytest
import sys

from particle.particle.utilities import str_with_unc


# Eventually
possibilites = (
    (1.234567,      .01,      None,     u'1.235 ± 0.010'),
    (1.234567e-9,   .01e-9,   None,     u'1.235e-09 ± 1.0e-11'),
    (1.234567e9,    .04e9,    None,     u'1.23e+09 ± 4e+07'),
    (0.001,         .00001,   None,     u'1.000e-03 ± 1.0e-05'),
    (0.00099,       .00001,   None,     u'9.90e-04 ± 1.0e-05'),
    (99,            .24,      None,     u'99.00 ± 0.24'),
    (100,           .25,      None,     u'100.0 ± 0.2'),
    (101,           .26,      None,     u'101.0 ± 0.3'),
    (.00001231,     .000002,  .000004,  u'1.23e-05 + 2.0e-06 - 4.0e-06'),
    (1234.5,        .03,      .03,      u'1234.50 ± 0.03'),
    (1234.5,        5,        5,        u'1234 ± 5'),
    (1234.5,        2,        2,        u'1234.5 ± 2.0'),
)

@pytest.mark.parametrize("value,err_u,err_l,test_str", possibilites)
def test_unc_printout(value, err_u, err_l, test_str):

    if sys.version_info < (3,0):
        test_str = test_str.replace(u'±', u'+/-')

    assert str_with_unc(value, err_u, err_l) == test_str
