#!/usr/bin/env python
# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.
"""This script generates the PDGID<->LHCb name mapping using the table from the LHCb DDDB package."""

from __future__ import annotations

import csv
import datetime as dt

import requests


def download_table(
    url="https://gitlab.cern.ch/lhcb-conddb/DDDB/-/raw/master/param/ParticleTable.txt",
):
    r = requests.get(url)
    r.raise_for_status()

    lines = r.text.split("\n")

    return [line.split() for line in filter(lambda x: x and x[0] == " ", lines)]


def main():
    date = dt.datetime.today().strftime("%Y-%m-%d")
    table = download_table()
    lhcb_names = {int(pdg_id): name for name, _, pdg_id, *_ in table}

    with open("src/particle/lhcb/data/pdgid_to_lhcbname.csv", "w") as out_csv:
        out_csv.write(
            f"# (c) Scikit-HEP project - Particle package data file - pdgid_to_lhcbname.csv - {date}\n"
        )
        writer = csv.DictWriter(
            out_csv, fieldnames=("PDGID", "STR"), lineterminator="\n"
        )
        writer.writeheader()

        for pid, name in sorted(
            lhcb_names.items(), key=lambda x: (abs(int(x[0])), -int(x[0]))
        ):
            writer.writerow({"PDGID": pid, "STR": name})


if __name__ == "__main__":
    main()
