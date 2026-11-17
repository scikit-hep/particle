# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import csv

import pytest

from particle import Particle
from particle.exceptions import MatchingIDNotFound
from particle.lhcb import LHCbName2PDGIDBiMap, from_lhcb_name, to_lhcb_name
from particle.lhcb.data import basepath
from particle.pdgid import PDGID

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
    ("He3", 1000020030),
    ("He3~", -1000020030),
    ("C12", 1000060120),
    ("Pb208", 1000822080),
    # ("X_1(3872)", 9920443),
)

# Names in the LHCb table with no counterpart in the PDG particle data tables
lhcb_only_names = (
    ("Intermediate", -99000000),
    ("qv", 4900101),
    ("SLscc", 99000100),
    ("SL~", -99000110),
    ("SL_2+", 99000122),
    ("LL", 99000210),
    ("LL_1-", -99000221),
)


def _lhcb_map_entries() -> list[tuple[str, int]]:
    with (basepath / "pdgid_to_lhcbname.csv").open() as f:
        return [
            (row["STR"], int(row["PDGID"]))
            for row in csv.DictReader(line for line in f if not line.startswith("#"))
        ]


@pytest.mark.parametrize(("name", "pid"), lhcb_style_names)
def test_from_lhcb_name(name: str, pid: int) -> None:
    assert from_lhcb_name(name).pdgid == pid


@pytest.mark.parametrize(("name", "pid"), lhcb_style_names)
def test_to_lhcb_name(name: str, pid: int) -> None:
    assert to_lhcb_name(Particle.from_pdgid(pid)) == name


@pytest.mark.parametrize(("name", "pid"), lhcb_only_names)
def test_lhcb_only_names(name: str, pid: int) -> None:
    assert LHCbName2PDGIDBiMap[name] == pid
    assert LHCbName2PDGIDBiMap[PDGID(pid)] == name


def test_lhcb_map_round_trip() -> None:
    entries = _lhcb_map_entries()

    # The mapping is one-to-one
    assert len({name for name, _ in entries}) == len(entries)
    assert len({pid for _, pid in entries}) == len(entries)
    assert len(LHCbName2PDGIDBiMap) == len(entries)

    for name, pid in entries:
        assert LHCbName2PDGIDBiMap[name] == pid
        assert LHCbName2PDGIDBiMap[PDGID(pid)] == name


def test_lhcb_nuclei_names() -> None:
    # The LHCb table names nuclei without an excitation energy suffix,
    # e.g. "Al27" rather than the "Al27[0.0]" of older versions of the table
    nuclei = [(n, pid) for n, pid in _lhcb_map_entries() if PDGID(pid).is_nucleus]
    assert nuclei
    assert all("[" not in name for name, _ in nuclei)

    assert LHCbName2PDGIDBiMap["Al27"] == 1000130270
    with pytest.raises(MatchingIDNotFound):
        LHCbName2PDGIDBiMap["Al27[0.0]"]
