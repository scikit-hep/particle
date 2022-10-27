#!/usr/bin/env python
# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.
"""
Script to generate the pdgid_to_corsika7id.csv conversion table from Corsika7ID to PDGID and vice-versa.
This script should be kept, so the table won't need to be hand-edited in the future.
"""
from __future__ import annotations

import csv
import datetime as dt
import pathlib

from particle import Particle, ParticleNotFound
from particle.shared_literals import common_particles

# Pairs of matching (Corsika7ID, PDGID),
# if the Corsika7ID has a matching PDGID, if not
# then (Corsika7ID, str), with the string from
# the Corsika7 user guide
corsica_pdg_id = [
    (1, common_particles["gamma"]),
    (50, common_particles["omega_782"]),
    (2, common_particles["e_plus"]),
    (51, common_particles["rho_770_0"]),
    (3, common_particles["e_minus"]),
    (52, common_particles["rho_770_plus"]),
    (53, common_particles["rho_770_minus"]),
    (5, common_particles["mu_plus"]),
    (54, common_particles["Delta_1232_pp"]),
    (6, common_particles["mu_minus"]),
    (55, common_particles["Delta_1232_plus"]),
    (7, common_particles["pi_0"]),
    (56, common_particles["Delta_1232_0"]),
    (8, common_particles["pi_plus"]),
    (57, common_particles["Delta_1232_minus"]),
    (9, common_particles["pi_minus"]),
    (58, common_particles["Delta_1232_mm_bar"]),
    (10, common_particles["K_L_0"]),
    (59, common_particles["Delta_1232_minus_bar"]),
    (11, common_particles["K_plus"]),
    (60, common_particles["Delta_1232_0_bar"]),
    (12, common_particles["K_minus"]),
    (61, common_particles["Delta_1232_plus_bar"]),
    (13, common_particles["neutron"]),
    (62, common_particles["Kst_892_0"]),
    (14, common_particles["proton"]),
    (63, common_particles["Kst_892_plus"]),
    (15, common_particles["antiproton"]),
    (64, common_particles["Kst_892_minus"]),
    (16, common_particles["K_S_0"]),
    (65, common_particles["Kst_892_0_bar"]),
    (17, common_particles["eta"]),
    (66, common_particles["nu_e"]),
    (18, common_particles["Lambda"]),
    (67, common_particles["nu_e_bar"]),
    (19, common_particles["Sigma_plus"]),
    (68, common_particles["nu_mu"]),
    (20, common_particles["Sigma_0"]),
    (69, common_particles["nu_mu_bar"]),
    (21, common_particles["Sigma_minus"]),
    (22, common_particles["Xi_0"]),
    (71, "η → γγ"),
    (23, common_particles["Xi_minus"]),
    (72, "η → 3π◦"),
    (24, common_particles["Omega_minus"]),
    (73, "η → π+π−π◦"),
    (25, common_particles["antineutron"]),
    (74, "η → π+π−γ"),
    (26, common_particles["Lambda_bar"]),
    (75, "μ+ add. info."),
    (27, common_particles["Sigma_minus_bar"]),
    (76, "μ− add. info."),
    (28, common_particles["Sigma_0_bar"]),
    (29, common_particles["Sigma_plus_bar"]),
    (85, "decaying μ+ at start"),
    (30, common_particles["Xi_0_bar"]),
    (86, "decaying μ− at start"),
    (31, common_particles["Xi_plus_bar"]),
    (32, common_particles["Omega_plus_bar"]),
    (95, "decaying μ+ at end"),
    (48, common_particles["etap_958"]),
    (49, common_particles["phi_1020"]),
    (96, "decaying μ− at end"),
    (116, common_particles["D_0"]),
    (155, common_particles["Xi_cp_minus_bar"]),
    (117, common_particles["D_plus"]),
    (156, common_particles["Xi_cp_0_bar"]),
    (118, common_particles["D_minus"]),
    (157, common_particles["Omega_c_0_bar"]),
    (119, common_particles["D_0_bar"]),
    (120, common_particles["D_s_plus"]),
    (161, common_particles["Sigma_c_2455_pp"]),
    (121, common_particles["D_s_minus"]),
    (162, common_particles["Sigma_c_2455_plus"]),
    (122, common_particles["eta_c_1S"]),
    (163, common_particles["Sigma_c_2455_0"]),
    (123, common_particles["Dst_2007_0"]),
    (124, common_particles["Dst_2010_plus"]),
    (171, common_particles["Sigma_c_2455_mm_bar"]),
    (125, common_particles["Dst_2010_minus"]),
    (172, common_particles["Sigma_c_2455_minus_bar"]),
    (126, common_particles["Dst_2007_0_bar"]),
    (173, common_particles["Sigma_c_2455_0_bar"]),
    (127, common_particles["D_sst_plus"]),
    (128, common_particles["D_sst_minus"]),
    (176, common_particles["B_0"]),
    (177, common_particles["B_plus"]),
    (130, common_particles["Jpsi_1S"]),
    (178, common_particles["B_minus"]),
    (131, common_particles["tau_plus"]),
    (179, common_particles["B_0_bar"]),
    (132, common_particles["tau_minus"]),
    (180, common_particles["B_s_0"]),
    (133, common_particles["nu_tau"]),
    (181, common_particles["B_s_0_bar"]),
    (134, common_particles["nu_tau_bar"]),
    (182, common_particles["B_c_plus"]),
    (183, common_particles["B_c_minus"]),
    (137, common_particles["Lambda_c_plus"]),
    (184, common_particles["Lambda_b_0"]),
    (138, common_particles["Xi_c_plus"]),
    (185, common_particles["Sigma_b_minus"]),
    (139, common_particles["Xi_c_0"]),
    (186, common_particles["Sigma_b_plus"]),
    (140, common_particles["Sigma_c_2455_pp"]),
    (187, common_particles["Xi_b_0"]),
    (141, common_particles["Sigma_c_2455_plus"]),
    (188, common_particles["Xi_b_minus"]),
    (142, common_particles["Sigma_c_2455_0"]),
    (189, common_particles["Omega_b_minus"]),
    (143, common_particles["Xi_cp_plus"]),
    (190, common_particles["Lambda_b_0_bar"]),
    (144, common_particles["Xi_cp_0"]),
    (191, common_particles["Sigma_b_plus_bar"]),
    (145, common_particles["Sigma_c_2455_0"]),
    (192, common_particles["Sigma_b_minus_bar"]),
    (193, common_particles["Xi_b_0_bar"]),
    (149, common_particles["Lambda_c_minus_bar"]),
    (194, common_particles["Xi_b_plus_bar"]),
    (150, common_particles["Xi_c_minus_bar"]),
    (195, common_particles["Omega_b_plus_bar"]),
    (151, common_particles["Xi_c_0_bar"]),
    (152, common_particles["Sigma_c_2455_mm_bar"]),
    (153, common_particles["Sigma_c_2455_minus_bar"]),
    (154, common_particles["Sigma_c_2455_0_bar"]),
]


def dump_pdgid_to_corsika7(file: pathlib.Path | None = None) -> None:
    """
    Generates the conversion .csv file with the patching PDGID to Corsika7ID under 'src/particle/data/pdgid_to_corsika7id.csv'
    (if file is None, else in the specified path).
    """
    # Loop over all thinkable values and only add them if the PDG ID exists
    for a in range(2, 56 + 1):
        for z in range(0, a + 1):
            corsikaid = a * 100 + z
            try:
                corsica_pdg_id.append(
                    (corsikaid, int(Particle.from_nucleus_info(a=a, z=z).pdgid))
                )
            except ParticleNotFound:
                pass

    if file is None:
        file = (
            pathlib.Path(__file__)
            .parent.parent.resolve()
            .absolute()
            .joinpath("src/particle/data/pdgid_to_corsika7id.csv")
        )

    date = dt.datetime.today().strftime("%Y-%m-%d")

    with open(
        file,
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        csvfile.write(
            f"# (c) Scikit-HEP project - Particle package data file - pdgid_to_corsika7id.csv - {date}\n"
        )
        csvfile.write(
            "# Auto generated by 'admin/dump_pdgid_to_corsika7.py'\n",
        )

        writer = csv.writer(csvfile)
        # Header
        writer.writerow(("PDGID", "CORSIKA7ID"))
        for corsikaid, pdgid in sorted(corsica_pdg_id, key=lambda x: x[0]):
            if isinstance(pdgid, int):
                writer.writerow((pdgid, corsikaid))


if __name__ == "__main__":
    dump_pdgid_to_corsika7()
