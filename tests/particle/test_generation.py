# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest

# Requires pandas
pd = pytest.importorskip("pandas")

from collections import Counter

from particle import data
from particle.particle.convert import produce_files


FILES = ["particle2020.csv", "particle2021.csv"]


def test_generate(tmp_path):
    "This verifies that the input and output files match."

    particle2020 = tmp_path / "particle2020.csv"
    particle2021 = tmp_path / "particle2021.csv"

    produce_files(particle2020, particle2021, "DUMMY", "2021")

    """
    # No longer test this file, which eventually will be removed
    particle2018_data = data.basepath / "particle2018.csv"
    with particle2018.open() as src, particle2018_data as res:
        src = [l for l in src.readlines() if not l.startswith("#")]
        res = [l for l in res.readlines() if not l.startswith("#")]
        assert src == res
    """

    particle2021_data = data.basepath / "particle2021.csv"
    with particle2021.open() as src, particle2021_data.open() as res:
        src = [l for l in src.readlines() if not l.startswith("#")]
        res = [l for l in res.readlines() if not l.startswith("#")]
        assert src == res


@pytest.mark.parametrize("filename", FILES)
def test_csv_file_duplicates(filename):
    with data.basepath / filename as particle_data:
        p = pd.read_csv(particle_data, comment="#")

    duplicates = {item for item, count in Counter(p.ID).items() if count > 1}
    assert duplicates == set()


@pytest.mark.parametrize("filename", FILES)
def test_csv_file_has_latex(filename):
    with data.basepath / filename as particle_data:
        p = pd.read_csv(particle_data, comment="#")

    assert p[p.Latex == ""].empty
