# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

# Requires pandas
pd = pytest.importorskip("pandas")

from collections import Counter

from particle import data
from particle.particle.convert import produce_files

FILES = ["particle2021.csv", "particle2022.csv"]


def test_generate(tmp_path):
    "This verifies that the input and output files match."

    particle2021 = tmp_path / "particle2021.csv"
    particle2022 = tmp_path / "particle2022.csv"

    produce_files(particle2021, particle2022, "DUMMY", "2022")

    """
    # No longer test this file, which eventually will be removed
    particle2018_data = data.basepath / "particle2018.csv"
    with particle2018.open() as src, particle2018_data as res:
        src = [l for l in src.readlines() if not l.startswith("#")]
        res = [l for l in res.readlines() if not l.startswith("#")]
        assert src == res
    """

    particle2022_data = data.basepath / "particle2022.csv"
    with particle2022.open() as src, particle2022_data.open() as res:
        src = [line for line in src.readlines() if not line.startswith("#")]
        res = [line for line in res.readlines() if not line.startswith("#")]
        assert src == res


@pytest.mark.parametrize("filename", FILES)
def test_csv_file_duplicates(filename):
    particle_data = data.basepath / filename
    p = pd.read_csv(particle_data, comment="#")

    duplicates = {item for item, count in Counter(p.ID).items() if count > 1}
    assert duplicates == set()


@pytest.mark.parametrize("filename", FILES)
def test_csv_file_has_latex(filename):
    particle_data = data.basepath / filename
    p = pd.read_csv(particle_data, comment="#")

    assert p[p.Latex == ""].empty
