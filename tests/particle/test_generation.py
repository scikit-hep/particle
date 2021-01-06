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


FILES = ["particle2019.csv", "particle2020.csv"]


def test_generate(tmp_path):
    "This verifies that the input and output files match."

    particle2019 = tmp_path / "particle2019.csv"
    particle2020 = tmp_path / "particle2020.csv"

    produce_files(particle2019, particle2020, "DUMMY", "2020")

    """
    # No longer test this file, which eventually will be removed
    particle2018_data = data.open_text(data, "particle2018.csv")
    with particle2018.open() as src, particle2018_data as res:
        src = [l for l in src.readlines() if not l.startswith("#")]
        res = [l for l in res.readlines() if not l.startswith("#")]
        assert src == res
    """

    particle2020_data = data.open_text(data, "particle2020.csv")
    with particle2020.open() as src, particle2020_data as res:
        src = [l for l in src.readlines() if not l.startswith("#")]
        res = [l for l in res.readlines() if not l.startswith("#")]
        assert src == res


@pytest.mark.parametrize("filename", FILES)
def test_file_dup(filename):
    with data.open_text(data, filename) as particle_data:
        p = pd.read_csv(particle_data, comment="#")

    duplicates = {item for item, count in Counter(p.ID).items() if count > 1}
    assert duplicates == set()


@pytest.mark.parametrize("filename", FILES)
def test_file_has_latex(filename):
    with data.open_text(data, filename) as particle_data:
        p = pd.read_csv(particle_data, comment="#")

    assert p[p.Latex == ""].empty
