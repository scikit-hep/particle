from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture

from particle import Particle, data


def test_load_particle_table(benchmark: BenchmarkFixture) -> None:
    benchmark(Particle.load_table, data.basepath / "particle2025.csv")


def test_load_nuclei_append(benchmark: BenchmarkFixture) -> None:
    def load_two() -> None:
        Particle.load_table(data.basepath / "particle2025.csv")
        Particle.load_table(data.basepath / "nuclei2022.csv", append=True)

    benchmark(load_two)


def test_from_pdgid(benchmark: BenchmarkFixture) -> None:
    Particle.load_table(data.basepath / "particle2025.csv")
    table = [int(s.pdgid) for s in Particle.all()]

    def get_all(listing: list[int]) -> None:
        for pdgid in listing:
            Particle.from_pdgid(pdgid)

    benchmark(get_all, table)
