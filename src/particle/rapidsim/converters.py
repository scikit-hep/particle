# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import io
import os
from pathlib import Path

from ..converters.bimap import BiMap
from ..pdgid import PDGID
from . import data


def _load_from_dat(dat_file: Path) -> io.StringIO:
    """
    Parse a RapidSim ``particles.dat`` file and return a CSV-formatted
    :class:`io.StringIO` with ``PDGID,STR`` rows suitable for :class:`BiMap`.

    Each row in ``particles.dat`` provides a particle name and, when present
    (i.e. not ``---``), an antiparticle name.  The antiparticle is mapped to
    the negated PDG ID following the standard PDG sign convention.
    """
    lines: list[str] = ["PDGID,STR\n"]
    with dat_file.open(encoding="utf-8") as f:
        next(f)  # skip header line
        for line in f:
            parts = line.split()
            if len(parts) < 3:
                continue
            pdgid, part, anti = parts[0], parts[1], parts[2]
            lines.append(f"{pdgid},{part}\n")
            if anti != "---":
                lines.append(f"-{pdgid},{anti}\n")
    return io.StringIO("".join(lines))


def _build_bimap() -> BiMap[PDGID, str]:
    """
    Build the RapidSim name <-> PDG ID :class:`BiMap`.

    Attempts to load from ``$RAPIDSIM_ROOT/config/particles.dat`` first.
    Falls back to the bundled CSV file if not available.
    """
    rapidsim_root = os.environ.get("RAPIDSIM_ROOT")
    if rapidsim_root is not None:
        dat_file = Path(rapidsim_root) / "config" / "particles.dat"
        if dat_file.is_file():
            return BiMap(
                PDGID,
                str,
                converters=(int, str),
                filename=_load_from_dat(dat_file),
            )
    # Fall back to bundled CSV
    return BiMap(
        PDGID,
        str,
        converters=(int, str),
        filename=data.basepath / "pdgid_to_rapidsimname.csv",
    )


RapidSimName2PDGIDBiMap: BiMap[PDGID, str] = _build_bimap()
RapidSimName2PDGIDBiMap.__doc__ = """
Bi-directional map between PDG IDs and RapidSim particle names.

Built at import time by:
1. Reading ``$RAPIDSIM_ROOT/config/particles.dat`` if ``$RAPIDSIM_ROOT`` is set
   and the file is available
2. Falling back to the bundled CSV file otherwise

Examples
--------
>>> pdgid = RapidSimName2PDGIDBiMap['Bs0']
>>> pdgid
<PDGID: 531>

>>> from particle.pdgid import PDGID
>>> name = RapidSimName2PDGIDBiMap[PDGID(531)]
>>> name
'Bs0'
"""
