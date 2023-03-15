# Copyright (c) 2018-2023, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle.particle.utilities import (
    greek_letter_name_to_unicode,
    latex_name_unicode,
    str_with_unc,
)

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
