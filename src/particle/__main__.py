#!/usr/bin/env python
# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

import argparse
import sys

from . import __version__
from .particle import Particle
from .pdgid import PDGID


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="particle",
        description="Particle command line display utility. Has two modes.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(help="Subcommands")

    search = subparsers.add_parser(
        "search",
        help="Look up particles by PID or name (Ex.: python -m particle search D+ D-)",
    )
    search.add_argument("particle", nargs="+", help="Name(s) or ID(s)")

    pdgid = subparsers.add_parser(
        "pdgid", help="Print info from PID (Ex.: python -m particle pdgid 11 13)"
    )
    pdgid.add_argument("pdgid", nargs="+", help="ID(s)")

    opts = parser.parse_args()

    if "particle" in opts:
        for cand in opts.particle:
            if hasattr(cand, "decode"):
                cand = cand.decode("utf-8")

            try:
                value = int(cand)
            except ValueError:
                value = 0

            if value:
                particles = [Particle.from_pdgid(value)]
            else:
                particles = Particle.from_string_list(cand)

            if not particles:
                print("Particle", cand, "not found.")
                sys.exit(1)
            elif len(particles) == 1:
                print(particles[0].describe())
            else:
                for particle in particles:
                    print(repr(particle))

            print()

    if "pdgid" in opts:
        for value in opts.pdgid:
            p = PDGID(value)
            print(p)
            print(PDGID(value).info())


if __name__ == "__main__":
    main()
