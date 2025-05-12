# Copyright (c) 2018-2025, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle.particle.utilities import (
    greek_letter_name_to_unicode,
    latex_name_unicode,
    programmatic_name,
    str_with_unc,
)

possibilities = (
    # Particles
    ("d", "d", False),
    ("b~", "b_bar", False),
    ("nu(e)~", "nu_e_bar", False),
    ("tau+", "tau_plus", False),
    ("H0", "H_0", False),
    ("a(2)(1320)0", "a_2_1320_0", False),
    ("f(2)'(1525)", "f_2p_1525", False),
    ("Delta(1232)~--", "Delta_1232_mm_bar", False),
    ("a(0)(1450)0", "a_0_1450_0", False),
    ("K*(892)0", "Kst_892_0", False),
    ("K(2)*(1430)~0", "K_2st_1430_0_bar", False),
    ("D(2)*(2460)+", "D_2st_2460_plus", False),
    ("B(s2)*(5840)0", "B_s2st_5840_0", False),
    ("(dd)(1)", "dd_1", False),
    # Nuclei
    ("H4", "H4", True),
    ("He4", "He4", True),
    ("He4~", "He4_bar", True),
    ("C10", "C10", True),
    ("C10~", "C10_bar", True),
    ("Ag100", "Ag100", True),
    ("Ag100~", "Ag100_bar", True),
)


@pytest.mark.parametrize(("name", "value", "is_nucleus"), possibilities)
def test_programmatic_name(name, value, is_nucleus):
    assert programmatic_name(name, is_nucleus) == value


possibilities = (
    (1.234567, 0.01, None, "1.235 ± 0.010"),
    (1.234567e-9, 0.01e-9, None, "1.235e-09 ± 1.0e-11"),
    (1.234567e9, 0.04e9, None, "1.23e+09 ± 4e+07"),
    (0.001, 0.00001, None, "1.000e-03 ± 1.0e-05"),
    (0.00099, 0.00001, None, "9.90e-04 ± 1.0e-05"),
    (99, 0.24, None, "99.00 ± 0.24"),
    (100, 0.25, None, "100.0 ± 0.2"),
    (101, 0.26, None, "101.0 ± 0.3"),
    (0.00001231, 0.000002, 0.000004, "1.23e-05 + 2.0e-06 - 4.0e-06"),
    (1234.5, 0.03, 0.03, "1234.50 ± 0.03"),
    (1234.5, 5, 5, "1234 ± 5"),
    (1234.5, 2, 2, "1234.5 ± 2.0"),
    (1234.5, None, None, "1234.5"),
    (1234.5, None, 2, "1234.5"),
)


@pytest.mark.parametrize(("value", "err_u", "err_l", "test_str"), possibilities)
def test_unc_printout(value, err_u, err_l, test_str):
    assert str_with_unc(value, err_u, err_l) == test_str


possibilities = (
    ("\\omega", "ω"),
    ("\\Omega", "Ω"),
    ("\\Lambda", "Λ"),
    ("\\alpha_{x}^{0}\\beta\\Gamma(1234)\\Omega", "α_{x}^{0}βΓ(1234)Ω"),
)


@pytest.mark.parametrize(("name", "unicode_name"), possibilities)
def test_latex_name_unicode(name, unicode_name):
    assert latex_name_unicode(name) == unicode_name


def test_greek_letter_name_to_unicode():
    """
    Test the one exception that is not verified
    in the test "test_latex_name_unicode" above.
    """
    with pytest.raises(KeyError):
        _ = greek_letter_name_to_unicode("Lambda")
    with pytest.raises(KeyError):
        _ = greek_letter_name_to_unicode("NonExistent")
