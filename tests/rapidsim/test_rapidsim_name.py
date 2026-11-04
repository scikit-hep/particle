# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

from particle import Particle
from particle.exceptions import MatchingIDNotFound
from particle.rapidsim import (
    RapidSimName2PDGIDBiMap,
    from_rapidsim_name,
    to_rapidsim_name,
)

rapidsim_style_names = (
    ("e-", 11),
    ("e+", -11),
    ("mu-", 13),
    ("mu+", -13),
    ("pi0", 111),
    ("pi+", 211),
    ("pi-", -211),
    ("K+", 321),
    ("K-", -321),
    ("K0", 311),
    ("K0b", -311),
    ("KL", 130),
    ("KS", 310),
    ("D0", 421),
    ("D0b", -421),
    ("Ds+", 431),
    ("Ds-", -431),
    ("Bs0", 531),
    ("Bs0b", -531),
    ("p+", 2212),
    ("p-", -2212),
    ("Lambda0", 3122),
    ("Lambda0b", -3122),
    ("Lambdab0", 5122),
    ("Lambdab0b", -5122),
)


@pytest.mark.parametrize(("name", "pid"), rapidsim_style_names)
def test_from_rapidsim_name(name: str, pid: int) -> None:
    assert from_rapidsim_name(name).pdgid == pid


@pytest.mark.parametrize(("name", "pid"), rapidsim_style_names)
def test_to_rapidsim_name(name: str, pid: int) -> None:
    assert to_rapidsim_name(Particle.from_pdgid(pid)) == name


def test_bimap_lookup_by_pdgid() -> None:
    from particle.pdgid import PDGID

    assert RapidSimName2PDGIDBiMap[PDGID(531)] == "Bs0"
    assert RapidSimName2PDGIDBiMap[PDGID(-531)] == "Bs0b"


def test_bimap_lookup_by_name() -> None:
    from particle.pdgid import PDGID

    assert RapidSimName2PDGIDBiMap["Bs0"] == PDGID(531)
    assert RapidSimName2PDGIDBiMap["Bs0b"] == PDGID(-531)


def test_unknown_name_raises() -> None:
    with pytest.raises(MatchingIDNotFound):
        from_rapidsim_name("NotAParticle")
