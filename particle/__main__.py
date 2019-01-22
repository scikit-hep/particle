#!/usr/bin/env python

from __future__ import absolute_import,  print_function

from .particle import Particle
from .pdgid import PDGID

import argparse

parser = argparse.ArgumentParser(description='Particle utility')

subparsers = parser.add_subparsers(help="Subcommands")

search = subparsers.add_parser('search', help='Look up particles by PID or name')
search.add_argument('particle', nargs='+', help='Name(s) or ID(s)')

pdgid = subparsers.add_parser('pdgid', help='Print info from PID')
pdgid.add_argument('pdgid', nargs='+', help='ID(s)')

opts = parser.parse_args()

if 'particle' in opts:
    for value in opts.particle:
        if hasattr(value, 'decode'):
            value = value.decode('utf-8')

        if value.isnumeric():
            particle = Particle.from_pdgid(int(value))
        else:
            particle = Particle.from_string(value)

        print(particle.describe())
        print()

if 'pdgid' in opts:
    for value in opts.pdgid:
        p = PDGID(value)
        print(p)
        print(PDGID(value).info())

