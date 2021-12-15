from particle import Particle, data


def test_load_particle_table(benchmark):
    benchmark(Particle.load_table, data.basepath / "particle2021.csv")


def test_load_nuclei_append(benchmark):
    def load_two():
        Particle.load_table(data.basepath / "particle2021.csv")
        Particle.load_table(data.basepath / "nuclei2020.csv", append=True)

    benchmark(load_two)


def test_from_pdgid(benchmark):
    Particle.load_table(data.basepath / "particle2021.csv")
    table = [int(s.pdgid) for s in Particle.all()]

    def get_all(listing):
        for pdgid in listing:
            Particle.from_pdgid(pdgid)

    benchmark(get_all, table)
