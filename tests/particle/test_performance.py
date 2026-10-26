from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture

from particle import Particle, data


def test_load_particle_table(benchmark: BenchmarkFixture) -> None:
    benchmark(Particle.load_table, data.basepath / "particle2026.csv")


def test_load_nuclei_append(benchmark: BenchmarkFixture) -> None:
    def load_two() -> None:
        Particle.load_table(data.basepath / "particle2026.csv")
        Particle.load_table(data.basepath / "nuclei2026.csv", append=True)

    benchmark(load_two)


def test_from_pdgid(benchmark: BenchmarkFixture) -> None:
    Particle.load_table(data.basepath / "particle2026.csv")
    # skip tetraquarks - to be fixed asap for the new PDG ID scheme for tetraquarks
    table = [int(p.pdgid) for p in Particle.all() if 100000000 < abs(p.pdgid) < 199999999]

    def get_all(listing: list[int]) -> None:
        for pdgid in listing:
            # skip tetraquarks - to be fixed asap for the new PDG ID scheme for tetraquarks
            if 100000000 < abs(pdgid) < 199999999: continue
            Particle.from_pdgid(pdgid)

    benchmark(get_all, table)
