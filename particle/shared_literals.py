# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Helper module with common particle name aliases (PDGID class instances).
"""

from __future__ import absolute_import

# Names have to be valid identifiers.
# Values can be repeated.

common_particles = dict(
    # Gauge bosons
    photon=22,
    gamma=22,
    Z0=23,
    W_plus=24,
    W_minus=-24,

    # Leptons
    e_minus=11,
    e_plus=-11,
    mu_minus=13,
    mu_plus=-13,
    tau_minus=15,
    tau_plus=-15,
    nu_e=12,
    nu_mu=14,
    nu_tau=16,

    # Quarkonia
    jpsi=443,
    psi_2S=100443,
    Upsilon_1S=553,
    Upsilon_4S=300553,

    # Light mesons
    pi0=111,
    pi_plus=211,
    pi_minus=-211,
    K_L=130,
    K_S=310,
    K_plus=321,
    K_minus=-321,
    phi_1020=333,

    # Charm mesons
    D0=421,
    D_plus=411,
    D_minus=-411,
    Ds_plus=431,
    Ds_minus=-431,

    # Beauty mesons
    B0=511,
    B0_bar=-511,
    B_plus=521,
    B_minus=-521,
    Bs=531,
    Bs_bar=-531,

    # Beauty, charmed mesons
    Bc_plus=541,
    Bc_minus=-541,

    # Light baryons
    proton=2212,
    antiproton=-2212,
    neutron=2112,
    antineutron=-2112,
    Lambda=3122,
    Lambda_bar=-3122,
    Xi_minus=3312,
    Xi0=3322,
    Omega_minus=3334,

    # Charm baryons
    Lc_plus=4122,
    Lc_minus_bar=-4122,

    # Beauty baryons
    Lb0=5122,
    Lb0_bar=-5122,
    Xib0=5232,
    Xib_minus=5132,
    Omegab_minus=5332,
)
