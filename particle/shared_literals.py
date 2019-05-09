# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Helper (internal) module with common particle aliases.

See the particle.literals and the pdgid.literals submodules for the actually exposed aliases.
"""

from __future__ import absolute_import


# Names have to be valid identifiers.
# Values can be repeated.
common_particles = dict(
    # Gauge bosons
    photon=22,
    gamma=22,
    Z_0=23,
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
    nu_e_bar=-12,
    nu_mu=14,
    nu_mu_bar=-14,
    nu_tau=16,
    nu_tau_bar=-16,

    # Quarkonia
    Jpsi_1S=443,
    psi_2S=100443,
    eta_c_1S=441,
    eta_c_2S=100441,
    chi_c0_1P=10441,
    chi_c1_1P=20443,
    chi_c2_1P=445,
    Upsilon_1S=553,
    Upsilon_2S=100553,
    Upsilon_3S=200553,
    Upsilon_4S=300553,
    eta_b_1S=551,
    eta_b_2S=100551,
    chi_b0_1P=10551,
    chi_b1_1P=20553,
    chi_b2_1P=555,

    # Light mesons
    pi_0=111,
    pi_plus=211,
    pi_minus=-211,
    a_0_980_0=9000111,
    a_0_980_plus=9000211,
    rho_770_0=113,
    rho_770_plus=213,
    rho_770_minus=-213,
    a_1_1260_0=20113,
    a_1_1260_plus=20213,
    eta=221,
    etap_958=331,
    f_0_500=9000221,
    f_0_980=9010221,
    omega_782=223,
    phi_1020=333,
    K_L_0=130,
    K_S_0=310,
    K_plus=321,
    K_minus=-321,
    Kst_892_0=313,
    Kst_892_0_bar=-313,
    Kst_892_plus=323,
    Kst_892_minus=-323,
    K_0st_1430_0=10311,
    K_0st_1430_0_bar=-10311,
    K_0st_1430_plus=10321,
    K_0st_1430_minus=-10321,

    # Charm mesons
    D_0=421,
    D_0_bar=-421,
    D_plus=411,
    D_minus=-411,
    Dst_2007_0=423,
    Dst_2007_0_bar=-423,
    Dst_2010_plus=413,
    Dst_2010_minus=-413,
    D_s_plus=431,
    D_s_minus=-431,
    D_sst_plus=433,
    D_sst_minus=-433,
    D_s0st_2317_plus=10431,
    D_s0st_2317_minus=-10431,
    D_s1_2460_plus=20433,
    D_s1_2460_minus=-20433,
    D_s1_2536_plus=10433,
    D_s1_2536_minus=-10433,

    # Beauty mesons
    B_0=511,
    B_0_bar=-511,
    B_plus=521,
    B_minus=-521,
    B_s_0=531,
    B_s_0_bar=-531,

    # Beauty, charmed mesons
    B_c_plus=541,
    B_c_minus=-541,

    # Light baryons
    p=2212,
    proton=2212,
    p_bar=-2212,
    antiproton=-2212,
    n=2112,
    neutron=2112,
    n_bar=-2112,
    antineutron=-2112,
    Lambda=3122,
    Lambda_bar=-3122,
    Xi_minus=3312,
    Xi_0=3322,
    Omega_minus=3334,
    Delta_1232_minus=1114,
    Delta_1232_plus_bar=-1114,
    Delta_1232_0=2114,
    Delta_1232_0_bar=-2114,
    Delta_1232_plus=2214,
    Delta_1232_minus_bar=-2214,
    Delta_1232_pp=2224,
    Delta_1232_mm_bar=-2224,
    Lambda_1520=3124,
    Lambda_1520_bar=-3124,

    # Charm baryons
    Lambda_c_plus=4122,
    Lambda_c_minus_bar=-4122,

    # Beauty baryons
    Lambda_b_0=5122,
    Lambda_b_0_bar=-5122,
    Xi_b_0=5232,
    Xi_b_0_bar=-5232,
    Xi_b_minus=5132,
    Xi_b_plus_bar=-5132,
    Omega_b_minus=5332,
    Omega_b_plus_bar=-5332,
)
