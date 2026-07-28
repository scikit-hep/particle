#!/usr/bin/env python
# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

import argparse
import sys

from . import __version__
from .particle import Particle
from .particle.particle import InvalidParticle, ParticleNotFound
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

    subparsers = parser.add_subparsers(
        help="Subcommands", required=True, dest="command"
    )

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
            try:
                value = int(cand)
            except ValueError:
                value = 0

            try:
                if value:
                    particles = [Particle.from_pdgid(value)]
                else:
                    particles = Particle.findall(cand)
            except (InvalidParticle, ParticleNotFound):
                particles = []

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
            try:
                p = PDGID(value)
            except ValueError:
                print(f"Invalid PDG ID: {value!r}")
                sys.exit(1)
            print(p)
            print(p.info())


if __name__ == "__main__":
    main()
