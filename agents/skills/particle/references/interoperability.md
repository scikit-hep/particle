# Interoperability: MC IDs, names, hepunits, pandas

## MC generator ID classes

`PythiaID`, `Geant3ID` and `Corsika7ID` convert to and from `PDGID`
(`MatchingIDNotFound` is raised when no conversion exists; import it from
`particle.exceptions`). Geant4 uses the standard PDG IDs.

```python
from particle import PDGID, PythiaID, Geant3ID, Corsika7ID, Particle

pyid = PythiaID.from_pdgid(PDGID(9010221))  # <PythiaID: 10221>
pyid.to_pdgid()  # <PDGID: 9010221>
pdg = Geant3ID(8).to_pdgid()  # <PDGID: 211>
Particle.from_pdgid(pdg)  # pi+
cid = Corsika7ID(5).to_pdgid()  # <PDGID: -13>
```

**Corsika7 specifics** (Corsika8 uses Geant3 IDs):

```python
Corsika7ID.from_particle_description(6000)  # (Corsika7ID(6), False)  -> mu-
Corsika7ID.from_particle_description(
    -6000
)  # (Corsika7ID(6), True) — a (grand)mother particle
Corsika7ID(76).is_particle()  # False — additional info, not a particle
Corsika7ID(76).name()  # 'μ− add. info.'
```

Note: `Corsika7ID` arithmetic (e.g. `-Corsika7ID(5)`) returns a plain `int`,
unlike `-PDGID(...)`, which returns a `PDGID`.

**Custom ID classes** are easy if you know the mapping:

```python
from particle.mcid import MCParticleID


class MyGeneratorID(MCParticleID):
    _to_pdg_map = {1: 11, 2: -11, 3: 22}


MyGeneratorID(3).to_pdgid()  # <PDGID: 22>
MyGeneratorID.from_pdgid(PDGID(-11))  # <MyGeneratorID: 2>
```

The older converter objects in `particle.converters` (`Pythia2PDGIDBiMap`,
`Geant2PDGIDBiMap`, `Corsika72PDGIDBiMap`) are **deprecated since 1.0.0** — use
`to_pdgid()`/`from_pdgid()` instead.

## EvtGen and LHCb names

```python
Particle.from_evtgen_name("J/psi").pdgid  # <PDGID: 443>
Particle.from_pdgid(443).evtgen_name  # 'J/psi'
from particle import lhcb

lhcb.to_lhcb_name(Particle.from_pdgid(-531))  # 'B_s~0'
lhcb.from_lhcb_name("B_s~0")  # <Particle: name="B(s)~0", ...>
```

The `particle.lhcb` module also exposes `LHCbName2PDGIDBiMap` for direct
bidirectional lookups. EvtGen names are the ones used in `.dec` decay files.

## hepunits

`particle` returns plain floats in HEP standard units (MeV, ns, mm). The
`hepunits` package (a strict dependency) provides unit-aware quantities that
compare naturally:

```python
from particle import Particle
from hepunits import GeV, meter

p = Particle.from_pdgid(521)
5.2 * GeV < p.mass < 5.3 * GeV  # masses in MeV
p.ctau > 1 * meter  # ctau in mm
```

## pandas and tabulate

`Particle.to_list()` and `Particle.to_dict()` render a search as tabular data.
`to_list` returns rows with a header row first; `to_dict` is transposed (field
name → tuple of values). They accept the same filter/keyword arguments as
`findall`, plus `exclusive_fields`, `exclude_fields` and `n_rows`.

```python
rows = Particle.to_list(
    exclusive_fields=["pdgid", "name", "mass", "charge"],
    filter_fn=lambda p: p.pdgid.is_lepton and p.charge != 0,
    particle=True,
)
# rows[0] is the header; use with tabulate, or:
import pandas as pd

df = pd.DataFrame(rows[1:], columns=rows[0])
```

## NumPy and awkward arrays

`p.pdgid` is a `PDGID` (an `int` subclass). Convert with `int(p.pdgid)` when
you need a plain Python integer for NumPy/awkward arrays:

```python
import numpy as np
from particle import Particle

p = Particle.from_pdgid(521)
np.int64(int(p.pdgid))  # works fine
```

## Gotchas

- **Deprecated BiMaps** — do not use `Pythia2PDGIDBiMap` etc. from
  `particle.converters`; use the ID-class methods.
- **`MatchingIDNotFound`** import path is `particle.exceptions` (it subclasses
  `ValueError`); it is not re-exported at the top level.
- **Corsika7ID is not an antiparticle-preserving int** — arithmetic returns
  plain `int`s; negative Corsika IDs in files indicate mother particles, so use
  `from_particle_description`.
- **`Particle` has no decay data** — for branching fractions and decay chains
  use the separate `decaylanguage` package (see
  [particle-properties.md](particle-properties.md)).
