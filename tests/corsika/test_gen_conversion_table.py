from __future__ import annotations

import filecmp
import pathlib

from particle.corsika.gen_conversion_table import gen_conversion_table


def test_converion_table(tmp_path):
    path = tmp_path / "pdg_to_corsika7id.csv"
    gen_conversion_table(file=path)
    assert filecmp.cmp(
        path,
        pathlib.Path(__file__).parent.parent.parent.joinpath(
            "src/particle/data/pdgid_to_corsika7id.csv"
        ),
    )
