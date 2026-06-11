# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "particle", *args],
        capture_output=True,
        check=False,
        text=True,
    )


def test_no_subcommand_exits_2() -> None:
    result = run_cli()
    assert result.returncode == 2
    assert "usage:" in result.stderr.lower()


def test_search_valid_particle() -> None:
    result = run_cli("search", "D0")
    assert result.returncode == 0
    assert "Name: D0" in result.stdout


def test_search_unknown_pdgid() -> None:
    result = run_cli("search", "99999999")
    assert result.returncode == 1
    assert "not found" in result.stdout.lower()


def test_search_unknown_name() -> None:
    result = run_cli("search", "NoSuchParticle")
    assert result.returncode == 1
    assert "not found" in result.stdout.lower()


def test_pdgid_valid() -> None:
    result = run_cli("pdgid", "11")
    assert result.returncode == 0
    assert "11" in result.stdout


def test_pdgid_invalid() -> None:
    result = run_cli("pdgid", "abc")
    assert result.returncode == 1
    assert "Invalid PDG ID" in result.stdout
    assert "'abc'" in result.stdout
