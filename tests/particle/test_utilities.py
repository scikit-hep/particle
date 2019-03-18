# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest
import sys

from particle import Particle
from particle.particle.utilities import programmatic_name
from particle.particle.utilities import str_with_unc
from particle.shared_literals import common_particles
from particle.particle.particle import ParticleNotFound


def test_programmatic_name():
    """
    Test makes sure that all literals defined in particle.shared_literals
    match what is returned by Particle.programmatic_name.
    """
    for literal_name, pid in common_particles.items():
        if literal_name in ( 'photon', 'proton', 'antiproton', 'neutron', 'antineutron'):
            continue
        try:  # some particles in the literals may not be in the table (e.g the neutrinos as of 2018)
            p = Particle.from_pdgid(pid)
            assert Particle.from_pdgid(pid).programmatic_name == literal_name
        except ParticleNotFound:
            pass


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
