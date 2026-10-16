# Quantum numbers and classification

## Where they come from

- **From the data tables**: charge (`three_charge`), isospin `I`, `P`, `C`,
  `G`, `rank`, `status`.
- **Decoded from the PDG ID**: total spin `J`, orbital angular momentum `L`,
  spin `S` (mesons), and the quark content used by `PDGID` predicates.
- **Derived**: `spin_type`, `baryon_number`, `lepton_number`, `r_parity`,
  `strangeness`, `charmness`, `bottomness`, `topness`, `hypercharge`,
  `is_self_conjugate`, `is_unflavoured_meson`.

## Charge

```python
from particle import Particle

p = Particle.from_pdgid(521)
p.charge            # Fraction(1, 1)  — in units of the positron charge
p.three_charge      # 3 — int, 3 × charge; None if unknown
```

- `charge` is a `fractions.Fraction` (since 1.0.0); compare with `== 0` or
  convert with `float()`.
- `three_charge` is the int charge × 3 and matches the `Charge` enum
  (`Charge.p` = 3, `Charge.o` = 0, …); it can be used as a search term:
  `Particle.findall("pi", three_charge=Charge.p)`.

## Spin, parity, isospin

```python
from particle import Particle

p = Particle.from_pdgid(443)        # J/psi
p.J                  # Fraction(1, 1)
p.L, p.S             # meson orbital/spin quantum numbers, or None
p.I                  # Fraction(1, 2) — isospin
p.P, p.C, p.G        # Parity enums (Parity.p / Parity.m / Parity.u)
p.spin_type          # SpinType.Vector
```

- `J`, `L`, `S` are read off the PDG ID; `L`/`S` are `None` for non-mesons,
  and `J` is `None` when not meaningful.
- `P`, `C`, `G` are `Parity` enum values (`.p` = `+`, `.m` = `-`, `.u` =
  unknown/not applicable); they compare equal to their int values.
- `spin_type` (`Scalar`, `PseudoScalar`, `Vector`, `Axial`, `Tensor`,
  `PseudoTensor`) is relevant for bosons only; `SpinType.NonDefined` is
  returned otherwise, `SpinType.Unknown` when `(J, P)` is not known.

## Baryon, lepton and flavour numbers

```python
from particle import Particle

Particle.from_pdgid(2212).baryon_number   # 1  (proton)
Particle.from_pdgid(11).lepton_number     # 1  (electron); -1 for e+
Particle.from_pdgid(521).bottomness       # 1  (B+)
Particle.from_pdgid(321).strangeness      # 1  (K+)
Particle.from_pdgid(443).charmness        # 0  (J/psi is charmonium: net 0)
p = Particle.from_pdgid(443)
p.r_parity, p.hypercharge, p.topness, p.charmness   # 1, 0, 0, 0
p.is_self_conjugate                       # True for e.g. pi0, J/psi
p.is_unflavoured_meson                    # True for e.g. J/psi
```

These satisfy the usual relations — for example
`hypercharge = baryon_number + strangeness + charmness + bottomness + topness`
(as defined in the `hypercharge` docstring).

## Related enums

- **`Charge`** — charge × 3 (`Charge.pp`, `Charge.p`, `Charge.o`, …).
- **`Parity`** — `p` (+), `m` (−), `u` (unknown/relevant).
- **`SpinType`** — boson spin-parity families; `Unknown`, `NonDefined`.
- **`Inv`** — antiparticle behaviour: `Same` (self-conjugate), `Barred`
  (bar, e.g. proton), `ChargeInv` (charge flip, e.g. pi+ ↔ pi−).
- **`Status`** — PDG status: `Common` (established), `Rare`, `Unsure`,
  `Further`, `NotInPDT` (non-standard/exotic).

## Gotchas

- **Quantum numbers can disagree with the name/table for hand-built IDs** —
  `J`/`L`/`S` and quark content come from the ID encoding, so a fabricated ID
  yields inconsistent results. Use table lookups.
- **`charge`/`J`/`I` are `Fraction`s** — don't compare with `== 1.0` relying on
  float exactness; use `== 0`/`== 1` or `float()`.
- **`P`, `C`, `G` may be `Parity.u`** ("unknown/not applicable") rather than
  missing — check against the enum, not `None`.
- **`spin_type` is for bosons** — fermions and undefined spin states return
  `SpinType.NonDefined`/`SpinType.Unknown`.
