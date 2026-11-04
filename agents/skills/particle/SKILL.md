---
name: particle-usage
description: Use the Scikit-HEP `particle` library from Python code — PDG particle data lookups and searches (`Particle`), PDG ID queries (`PDGID` and the `particle.pdgid` functions), particle literals, MC generator ID classes (`PythiaID`, `Geant3ID`, `Corsika7ID`), EvtGen/LHCb name conversion, nuclei, and width/lifetime helpers. Use when writing application code that needs particle masses, widths, quantum numbers, antiparticle relations, or MC-ID conversions.
---

# Using the `particle` library

## Overview

`particle` is a pure-Python Scikit-HEP package providing a pythonic interface to the
Particle Data Group (PDG) particle data tables and the standard PDG particle
identification (ID) numbering scheme. It has two central objects:

- **`Particle`** — a full record for a particle (mass, width, lifetime, quantum
  numbers, quark content, PDG/LaTeX/EvtGen/LHCb names, status), with powerful
  search and look-up utilities.
- **`PDGID`** — an `int` subclass adding queries and classification on a PDG ID
  (is it a meson/baryon/lepton/nucleus? which quarks? what charge and spin?),
  mirrored by free-standing functions in `particle.pdgid`.

It also provides classes for the identification codes used by MC generators
(`PythiaID`, `Geant3ID`, `Corsika7ID`), name conversion maps (EvtGen, LHCb),
and `Particle`/`PDGID` literals for common particles.

All data tables ship inside the package and are loaded lazily: importing
`particle` does not read any data. The table is loaded on the first lookup
(`from_pdgid`, `findall`, `all`, …).

## When to use it

- You need PDG numbers — mass, width, lifetime, `c*tau` — in analysis/plotting code.
- You need to interpret or classify PDG IDs: meson/baryon/lepton/nucleus, quark
  content, charge, spin.
- You need antiparticle relations or standardized names (PDG, LaTeX, HTML,
  EvtGen, LHCb, programmatic).
- You need to convert between PDG IDs and MC generator IDs (Pythia, Geant3,
  Corsika7).
- You want ready-made constants for common particles (literals).

## Core concepts

- **Two objects, one ID scheme.** `PDGID` wraps an integer; `Particle` wraps one
  row of the PDG data tables. A negative PDG ID is the antiparticle; `-pid`
  returns another `PDGID`.
- **The PDG ID encodes quantum numbers.** Classification, spin and quark content
  are decoded from the ID digits; other properties (`charge`, `I`, `P`, `C`,
  `G`, `rank`, `status`) come from the data tables.
- **Names.** `name` is display-ready (`'B+'`, `'B~0'`, `'K0'`), `pdg_name` is the
  PDG table name _without_ charge (`'B'`, `'K'`); LaTeX/HTML/EvtGen/programmatic
  variants exist too.
- **Search semantics.** A bare string is a _fuzzy_ substring search on `name`;
  keyword arguments match _exactly_; values may be callables;
  `particle=True/False` filters to particles/antiparticles.
- **Units.** Mass and width in MeV, `lifetime` in ns, `ctau` in mm. `charge`,
  `J` and `I` are `Fraction`s, not floats.
- **Lazy table.** `Particle.all()`, `table_names()` and `table_loaded()` inspect
  the loaded table; lookups trigger loading automatically.

## Essential patterns

```python
from particle import Particle, PDGID
from particle.pdgid import is_meson, has_charm

p = Particle.from_pdgid(521)  # look up by ID (see references/particle-properties.md)
Particle.findall("pi", charge=-1)  # fuzzy name + exact charge
Particle.findall(lambda q: q.pdgid.has_bottom and q.charge == 0)
is_meson(211)  # classify a bare number
has_charm(p.pdgid)  # pass the PDGID, not the Particle
```

For literals (`Particle`/`PDGID` aliases) and MC-ID conversions, see the
reference files below.

## Major gotchas

- **`pdg_name` ≠ `name`** — `pdg_name` has no charge; `from_name` needs an
  exact, unique match (`from_name("pi")` raises).
- **Exceptions** — `from_pdgid` raises `InvalidParticle` (malformed ID) or
  `ParticleNotFound` (valid but not in the table); MC ID conversions raise
  `MatchingIDNotFound` (a `ValueError`, imported from `particle.exceptions`).
- **`None` means unknown** — quarks/neutrinos have `mass=None`, quarks have
  `width=None`; `lifetime`/`ctau` are `None` when the width is unknown, but
  `inf` for stable particles (`width == 0`).
- **Fractions** — `charge`, `J`, `I` return `fractions.Fraction`;
  `three_charge` is the int charge × 3.
- **`particle.pdgid` functions take numbers**, not `Particle` objects
  (`is_meson(p.pdgid)`, not `is_meson(p)`).
- **Proton/neutron have two PDG IDs** (baryon form `2112`/`2212` and nucleus
  form `1000000010`/`1000010010`); equality considers both, `from_name("p")`
  returns the baryon form.
- **Converters** — the `particle.converters` BiMaps (`Pythia2PDGIDBiMap`, …)
  are deprecated since 1.0.0; use `X.to_pdgid()`/`X.from_pdgid()` instead.

## Reference files

| File                                                                   | Contents                                                                                                       |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [references/pdgid.md](references/pdgid.md)                             | `PDGID` queries, ID classification, validity, antiparticles, `particle.pdgid` functions                        |
| [references/particle-properties.md](references/particle-properties.md) | Particle lookups, properties, searches, literals, names, mass/width/lifetime, custom particles and data tables |
| [references/quantum-numbers.md](references/quantum-numbers.md)         | Charge, spin, parity, isospin, flavour quantum numbers, and the related enums                                  |
| [references/interoperability.md](references/interoperability.md)       | MC generator IDs, EvtGen/LHCb names, `hepunits`, pandas/tabulate                                               |

## Documentation

The repository's `README.md` is a full usage tutorial; `notebooks/ParticleDemo.ipynb`
contains worked examples. Docstrings on `Particle`, `PDGID`, `MCParticleID`,
`Corsika7ID` and the `particle.pdgid` functions carry precise semantics (units,
exceptions). `docs/CHANGELOG.md` lists user-visible changes and
`src/particle/data/README.rst` documents the bundled data files.
