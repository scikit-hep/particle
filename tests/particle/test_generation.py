# Copyright (c) 2018-2023, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import pytest

# Requires pandas
pd = pytest.importorskip("pandas")

from collections import Counter

from particle import data
from particle.particle import Particle
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
        src_filtered = [line for line in src.readlines() if not line.startswith("#")]
        res_filtered = [line for line in res.readlines() if not line.startswith("#")]
        assert src_filtered == res_filtered


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


check_nucleons = (
    (2212, 1000010010),
    (-2212, -1000010010),
    (2112, 1000000010),
    (-2112, -1000000010),
)


@pytest.mark.parametrize(("id_particle", "id_nucleus"), check_nucleons)
def test_nucleon_properties(id_particle, id_nucleus):
    """
    Protons and neutrons are both available in the particles table and in the nuclei table
    under IDs 2212 and 2112, and 1000010010 and 1000000010, respectively.
    This trivial test checks most of what is likely to change between PDG updates,
    to ensure consistency.
    """
    p_particle = Particle.from_pdgid(id_particle)
    p_nucleus = Particle.from_pdgid(id_nucleus)

    # Trivial replacement of IDs to avoid obvious irrelevant differences
    assert p_particle.describe().replace(
        f"{id_particle:<12}", f"{id_particle:<12}"
    ) == p_nucleus.describe().replace(f"{id_nucleus:<12}", f"{id_particle:<12}")
