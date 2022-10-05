# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle import Particle
from particle.lhcb import from_lhcb_name, to_lhcb_name

lhcb_style_names = (
    ("nu_tau", 16),
    ("nu_tau~", -16),
    ("eta_prime", 331),
    ("f'_2(1525)", 335),
    ("D*_s+", 433),
    ("D*_s-", -433),
    ("B_s0", 531),
    ("B_s~0", -531),
    ("Lambda_b0", 5122),
    ("Lambda_b~0", -5122),
    # ("X_1(3872)", 9920443),
)


@pytest.mark.parametrize("name,pid", lhcb_style_names)
def test_from_lhcb_name(name, pid):
    assert from_lhcb_name(name).pdgid == pid


@pytest.mark.parametrize("name,pid", lhcb_style_names)
def test_to_lhcb_name(name, pid):
    assert to_lhcb_name(Particle.from_pdgid(pid)) == name
