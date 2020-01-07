# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest

# Requires pandas
pd = pytest.importorskip("pandas")

from collections import Counter

from particle import data
from particle.particle.convert import produce_files


FILES = ["particle2008.csv", "particle2019.csv"]


def test_generate(tmp_path):
    "This verifies that the input and output files match."

    particle2008 = tmp_path / "particle2008.csv"
    particle2019 = tmp_path / "particle2019.csv"

    produce_files(particle2008, particle2019, "DUMMY", "2019")

    particle2008_data = data.open_text(data, "particle2008.csv")
    with particle2008.open() as src, particle2008_data as res:
        src = [l for l in src.readlines() if not l.startswith("#")]
        res = [l for l in res.readlines() if not l.startswith("#")]
        assert src == res

    particle2019_data = data.open_text(data, "particle2019.csv")
    with particle2019.open() as src, particle2019_data as res:
        src = [l for l in src.readlines() if not l.startswith("#")]
        res = [l for l in res.readlines() if not l.startswith("#")]
        assert src == res


@pytest.mark.parametrize("filename", FILES)
def test_file_dup(filename):
    particle_data = data.open_text(data, filename)
    p = pd.read_csv(particle_data, comment="#")

    duplicates = {item for item, count in Counter(p.ID).items() if count > 1}
    assert duplicates == set()


@pytest.mark.parametrize("filename", FILES)
def test_file_has_latex(filename):
    particle_data = data.open_text(data, filename)
    p = pd.read_csv(particle_data, comment="#")

    assert p[p.Latex == ""].empty
