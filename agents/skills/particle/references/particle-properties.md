# Particle: lookups, properties, searches and custom particles

`Particle` is a full record for one row of the PDG particle data tables. Prefer
the class methods for lookups; never guess properties by hand.

## Getting a particle

```python
from particle import Particle

p = Particle.from_pdgid(521)          # B+          (raises InvalidParticle / ParticleNotFound)
p = Particle.from_name("J/psi(1S)")   # exact, must match exactly one particle
p = Particle.from_evtgen_name("J/psi")
p = Particle.from_nucleus_info(z=2, a=4)      # He4; anti=True for the antinucleus
```

- `from_pdgid` raises `InvalidParticle` for malformed codes and
  `ParticleNotFound` for valid codes not present in the loaded tables.
- `from_name` requires an **exact, unique** match on `name`; ambiguous names
  raise `ParticleNotFound` (`from_name("pi")` fails because many particles
  start with `pi`).
- `from_nucleus_info(z, a, ...)` builds the nucleus ID from the atomic number
  and mass number; `z > a` or out-of-range inputs raise `InvalidParticle`.

## Useful properties

```python
p.pdgid              # the PDGID
p.name               # 'B+', 'B~0', 'K0', ... (charge + anti-tilde included)
p.pdg_name           # 'B', 'K'  — the PDG table name, WITHOUT charge
p.evtgen_name        # EvtGen name, e.g. 'B+'
p.latex_name         # r'B^{+}'
p.html_name          # HTML rendering of the LaTeX name
p.programmatic_name  # 'B_plus', 'B_0' — safe as a variable name
p.mass, p.mass_upper, p.mass_lower   # in MeV; None if unknown
p.width, p.width_upper, p.width_lower # in MeV; None if unknown
p.lifetime           # in ns (hbar/Gamma); inf for stable particles
p.ctau               # in mm
p.charge             # Fraction; p.three_charge is the int 3*charge
p.quarks, p.rank, p.status, p.anti_flag
p.is_name_barred, p.is_self_conjugate
p.describe()         # high-density human-readable summary
```

Quantum numbers (`I`, `J`, `L`, `S`, `P`, `C`, `G`, `spin_type`, flavour
numbers, …) are covered in [quantum-numbers.md](quantum-numbers.md).

Antiparticles: `p.invert()` (also `-p` and `~p`). Sorting a list of particles
puts the lowest `abs(PDGID)` first. `str(p)`/`repr(p)` are display-ready.

## Search and look-up

`Particle.findall(...)` returns a list, `Particle.finditer(...)` an iterator.
The first positional argument is either a callable `lambda p: ...` or a string,
which is matched **fuzzily** (substring) against the particle `name`. Keyword
arguments match **exactly** against any attribute/property and may themselves
be callables.

```python
from hepunits import meter

Particle.findall("pi", charge=-1)                      # fuzzy name + exact charge
Particle.findall(pdg_name="B", particle=True)          # exact match on PDG name
Particle.findall(pdg_name="B", charge=0, particle=True)
Particle.findall(lambda p: p.pdgid.has_bottom and p.charge == 0)
Particle.findall(lambda p: p.pdgid.is_meson and p.pdgid.has_strange
                            and p.ctau > 1 * meter, particle=True)
Particle.finditer(name="Omega", particle=False)        # exact name search
```

`particle=True` keeps only particles, `particle=False` only antiparticles, and
`None` (default) both. Valid keyword terms include `pdg_name`, `name`, `mass`,
`mass_upper/lower`, `width`, `width_upper/lower`, `charge`, `three_charge`,
`anti_flag`, `rank`, `I`, `J`, `G`, `P`, `C`, `quarks`, `status`. A callable as
a value receives the property (e.g. `mass=lambda m: m is not None and m > 5.2*GeV`).

### Fuzzy vs exact name search — a common trap

A bare string is a fuzzy substring search on `name`; a keyword is exact:

```python
Particle.finditer("Omega", particle=False)       # fuzzy: several Omega states
Particle.finditer(name="Omega", particle=False)  # exact: no match (name is 'Omega~+')
Particle.findall(pdg_name="Omega", particle=False)  # exact PDG name: 1 match
```

The string match is a **literal substring** test, not a glob: `"K[+-]"` and
`"pi*"` match nothing. Use `fnmatch` (or a regex) inside a callable for
patterns:

```python
import fnmatch
from particle import Particle

Particle.findall(lambda p: fnmatch.fnmatch(p.name, "K[+-]"))   # K+, K-
```

`finditer` is lazy — prefer it over `findall` for large scans.

## Ready-made literals

`particle.literals` holds `Particle` instances, `particle.pdgid.literals`
holds `PDGID` instances. Names use the programmatic form, e.g. `pi_plus`,
`D_0`, `Lambda_b_0` (check the module `__dir__`). Accessing a literal creates
the object on demand.

```python
from particle import literals as lp
from particle.pdgid import literals as lid

lp.pi_plus            # <Particle: name="pi+", pdgid=211, ...>
lid.pi_plus           # <PDGID: 211>
lp.Lambda_b_0.J       # Fraction(1, 2)
```

## Width, lifetime and c*tau helpers

Mass/width live in the table in MeV; lifetime and `ctau` are derived:

```python
from particle import width_to_lifetime, lifetime_to_width

width_to_lifetime(4.33e-10)      # 0.00152 ns   (input MeV, output ns)
lifetime_to_width(0.00152)       # 4.33e-10 MeV
width_to_lifetime(0)             # inf
# width_to_lifetime(-1)          # -> ValueError
```

`lifetime` is `None` when the width is unknown, and `inf` when the width is 0
(stable particles). `ctau` is in mm.

There is **no `is_stable` property** — test the lifetime directly:

```python
from particle import Particle

def is_stable(p: Particle) -> bool:
    return p.lifetime == float("inf")

is_stable(Particle.from_pdgid(11))      # True  (electron)
is_stable(Particle.from_pdgid(211))     # False (pion decays)
```

## Loading custom data tables

The default table is `particle2026.csv` followed by `nuclei2026.csv`. Append or
replace via `Particle.load_table`; data files are reachable through
`particle.data.basepath` (works even when the package runs from a zipapp):

```python
import particle.data as data

Particle.load_table("my_particles.csv", append=True)   # extend (file must exist; same CSV layout)
Particle.load_table("my_table.csv")                    # replace (default append=False)
Particle.load_table(data.basepath / "particle2026.csv")
Particle.table_names()    # names of loaded tables (triggers loading if needed)
Particle.table_loaded()   # check without triggering a load
```

## Creating user-defined particles

`Particle(...)` takes `(pdgid, pdg_name)` positionally plus optional fields.
Use sparingly: a meaningful PDG ID encodes quantum numbers, so a "made-up" ID
gives undefined or wrong properties, and `mass`/`width` are `None` unless you
supply them.

```python
p = Particle.empty()                    # <Particle: name="Unknown", pdgid=0, mass=None>
p = Particle(9912345, "MyPentaquark")
p = Particle(pdgid=9221132, pdg_name="Theta", three_charge=3, latex_name=r"\Theta^{+}")
```

Hand-built particles are **not** in the table (`findall` won't return them)
unless added via `load_table`.

## Gotchas

- **`pdg_name` ≠ `name`.** The PDG table name omits the charge; `name` adds it
  (and a `~` for barred antiparticles, e.g. `pdg_name='B'` → `name='B+'`).
  Use `name` for display and `pdg_name` for exact table-name matching.
- **`from_name` needs a unique exact match** — use `from_pdgid` or
  `findall`/`finditer` for ambiguous cases.
- **`None` means unknown.** Quarks/neutrinos have `mass=None`; quarks have
  `width=None`; `lifetime`/`ctau` are `None` when the width is unknown. Filter
  lambdas that touch these may raise `TypeError` — `findall` skips such
  particles, so write filters defensively.
- **Stable particles report infinite lifetime/ctau** (`width == 0` gives
  `inf`), not `None`; there is no `is_stable` — test `p.lifetime == float("inf")`.
- **No decay modes.** `Particle` carries identity, mass, width and quantum
  numbers — there is no `decay_modes`/branching-fraction attribute. For decay
  chains and branching fractions use the separate `decaylanguage` package.
- **Hand-built particles** have `None` mass/width and properties derived from
  the ID; they are not in the table unless added via `load_table`.
