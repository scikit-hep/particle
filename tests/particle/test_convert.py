# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest

# Requires pandas
pd = pytest.importorskip("pandas")

from particle.particle.convert import get_from_pdg_mcd

try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path


DIR = Path(__file__).parent.resolve()


def test_get_from_pdg_mcd():
    with (DIR / "../data/test_PDG_mcd_file_duplicates.mcd").open() as f:
        with pytest.raises(AssertionError):
            get_from_pdg_mcd(f)
