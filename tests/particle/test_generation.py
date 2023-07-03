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
from particle.pdgid import (
    is_diquark,
    is_dyon,
    is_excited_quark_or_lepton,
    is_generator_specific,
    is_lepton,
    is_meson,
    is_pentaquark,
    is_Qball,
    is_quark,
    is_Rhadron,
    is_sm_lepton,
    is_special_particle,
    is_SUSY,
    is_technicolor,
    three_charge,
)

FILES = ["particle2022.csv", "particle2023.csv"]


def test_generate(tmp_path):
    "This verifies that the input and output files match."

    particle2022 = tmp_path / "particle2022.csv"
    particle2023 = tmp_path / "particle2023.csv"

    produce_files(particle2022, particle2023, "DUMMY", "2023")

    particle2023_data = data.basepath / "particle2023.csv"
    with particle2023.open() as src, particle2023_data.open() as res:
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


def test_None_masses():
    "Only certain specific particles should have None masses."
    none_masses = {
        100321,
        -100321,  # K(1460)+
    }
    for p in Particle.all():
        pdgid = p.pdgid
        if pdgid in none_masses:
            continue

        if (
            is_Qball(pdgid)
            or is_Rhadron(pdgid)
            or is_SUSY(pdgid)
            or is_diquark(pdgid)
            or is_dyon(pdgid)
            or is_excited_quark_or_lepton(pdgid)
            or is_generator_specific(pdgid)
            or (is_lepton(pdgid) and three_charge(pdgid) == 0)
            or (is_lepton(pdgid) and not is_sm_lepton(pdgid))  # neutrinos
            or (  # 4-th generation leptons
                is_meson(pdgid) and (abs(pdgid) // 1000000 % 10 == 9)
            )
            or is_pentaquark(  # Mesons with PDGIDs of the kind 9XXXXXX are not experimentally well-known
                pdgid
            )
            or is_quark(pdgid)
            or is_special_particle(pdgid)
            or is_technicolor(pdgid)
        ):
            continue

        assert p.mass is not None


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
