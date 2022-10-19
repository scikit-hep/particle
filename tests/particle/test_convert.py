# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

# Requires pandas
pd = pytest.importorskip("pandas")

from pathlib import Path

from particle.particle.convert import get_from_pdg_mcd

DIR = Path(__file__).parent.resolve()


def test_get_from_pdg_mcd():
    with (DIR / "../data/test_PDG_mcd_file_duplicates.mcd").open() as f:
        with pytest.raises(AssertionError):
            get_from_pdg_mcd(f)
