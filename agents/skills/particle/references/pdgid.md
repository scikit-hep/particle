# PDGID: queries, classification and antiparticles

`PDGID` is a subclass of `int`, so it can be used anywhere an `int` is
expected. A negative ID represents the antiparticle.

```python
from particle import PDGID, Particle

pid = PDGID(211)
pid.is_meson          # True
pid.charge            # Fraction(1, 1) (a Fraction, not a float)
pid.J                 # Fraction(0, 1)
pid.has_bottom        # False
pid.is_valid          # True
PDGID(99999999).is_valid          # False
-PDGID(211)                        # <PDGID: -211>
~PDGID(211)                        # also <PDGID: -211>
PDGID(323).info()                  # one property per line, for inspection
```

## What a PDG ID encodes

The PDG numbering scheme is a signed integer whose digits encode the particle's
quantum numbers (e.g. meson spin, orbital angular momentum, quark content,
nucleus composition). This means classification and spin are decoded *from the
ID*, and `PDGID` never needs the data tables.

Properties and their meaning:

- **Classification**: `is_meson`, `is_baryon`, `is_lepton`, `is_quark`,
  `is_hadron`, `is_nucleus`, `is_pentaquark`, `is_diquark`,
  `is_gauge_boson_or_higgs`, `is_sm_*` (Standard Model subset), `is_SUSY`,
  `is_technicolor`, `is_special_particle`, `is_generator_specific`,
  `is_Qball`, `is_Rhadron`, `is_excited_quark_or_lepton`, `is_dyon`.
- **Flavour content**: `has_up`, `has_down`, `has_strange`, `has_charm`,
  `has_bottom`, `has_top`, `has_fundamental_anti`.
- **Charge and spin**: `charge` (Fraction), `three_charge` (int × 3),
  `j_spin`, `l_spin`, `s_spin`, `J`, `L`, `S`, `A`, `Z`, `abspid`.

## Validity

`PDGID.is_valid` is `False` for codes outside the PDG scheme (e.g.
`PDGID(99999999)`); its repr shows `(is_valid==False)`. Raising operations such
as `Particle.from_pdgid` check validity and raise `InvalidParticle` for invalid
codes (see [particle-properties.md](particle-properties.md)).

## Antiparticles

- Negative IDs are antiparticles. `-PDGID(211)` gives `<PDGID: -211>`.
- `~pid` is an alias for `-pid` and returns a `PDGID` too.
- `abspid` strips the sign (e.g. for keying or sorting).
- Note: `PDGID` operations preserve the class (`-pid` is a `PDGID`), unlike
  `Corsika7ID` arithmetic (see [interoperability.md](interoperability.md)).

## Free-standing `particle.pdgid` functions

Every `PDGID` property exists as a standalone function in `particle.pdgid`,
operating on any int-like value (useful for composition):

```python
from particle.pdgid import is_meson, has_charm, has_bottom
from particle import Particle

is_meson(211)                        # True  (plain int works)
is_meson(Particle.from_pdgid(211).pdgid)   # pass the PDGID, not the Particle
has_charm(4122)                      # True
is_heavy = lambda x: has_charm(x) or has_bottom(x)
```

Important: these functions accept a `SupportsInt` — pass `p.pdgid`, **not** the
`Particle` object (passing a `Particle` raises `TypeError`).

## Gotchas

- **Two PDG IDs for proton and neutron.** The baryon forms `2112`/`2212`
  and the nucleus forms `1000000010`/`1000010010` describe the same particles.
  `Particle.__eq__` treats both as equal, but lookup/hash prefer the baryon
  form; `Particle.from_name("p")` returns the baryon representation, while
  `Particle.findall(pdg_name="p")` returns both.
- **A "random" ID gives wrong or `None` properties.** Quantum numbers are
  decoded from the digits, so inventing an ID yields inconsistent results
  (e.g. `Particle(9912345, "X").pdgid.is_pentaquark` is `False`).
- **`J`/`L`/`S` may be `None`** for non-mesons; `is_valid` is `False` for
  out-of-scheme codes. Prefer looking particles up from the table rather than
  constructing IDs by hand.
