# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

# Requires pandas
pd = pytest.importorskip("pandas")

from pathlib import Path

from particle.particle.convert import get_from_pdg_txt

DIR = Path(__file__).parent.resolve()


def test_get_from_pdg_txt() -> None:
    with (
        (DIR / "../data/test_PDG_txt_file_duplicates.txt").open() as f,
        pytest.raises(AssertionError),
    ):
        get_from_pdg_txt(f)
