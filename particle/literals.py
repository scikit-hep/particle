# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Helper module with common particle name aliases (PDGID class instances).
"""

from __future__ import absolute_import

from .pdgid import PDGID


# Gauge bosons
photon = PDGID(22)
gamma = photon
Z0 = PDGID(23)
W_plus = PDGID(24)
W_minus = PDGID(-24)

# Leptons
e_minus = PDGID(11)
e_plus = PDGID(-11)
mu_minus = PDGID(13)
mu_plus = PDGID(-13)
tau_minus = PDGID(15)
tau_plus = PDGID(-15)
nu_e = PDGID(12)
nu_mu = PDGID(14)
nu_tau = PDGID(16)

# Quarkonia
jpsi = PDGID(443)
psi_2S = PDGID(100443)
Upsilon_1S = PDGID(553)
Upsilon_4S = PDGID(300553)

# Light mesons
pi0 = PDGID(111)
pi_plus = PDGID(211)
pi_minus = PDGID(-211)
K_L = PDGID(130)
K_S = PDGID(310)
K_plus = PDGID(321)
K_minus = PDGID(-321)
phi_1020 = PDGID(333)

# Charm mesons
D0 = PDGID(421)
D_plus = PDGID(411)
D_minus = PDGID(-411)
Ds_plus = PDGID(431)
Ds_minus = PDGID(-431)

# Beauty mesons
B0 = PDGID(511)
B0_bar = PDGID(-511)
B_plus = PDGID(521)
B_minus = PDGID(-521)
Bs = PDGID(531)
Bs_bar = PDGID(-531)

# Beauty, charmed mesons
Bc_plus = PDGID(541)
Bc_minus = PDGID(-541)

# Light baryons
proton = PDGID(2212)
antiproton = PDGID(-2212)
neutron = PDGID(2112)
antineutron = PDGID(-2112)
Lambda = PDGID(3122)
Lambda_bar = PDGID(-3122)
Xi_minus = PDGID(3312)
Xi0 = PDGID(3322)
Omega_minus = PDGID(3334)

# Charm baryons
Lc_plus = PDGID(4122)
Lc_minus_bar = PDGID(-4122)

# Beauty baryons
Lb0 = PDGID(5122)
Lb0_bar = PDGID(-5122)
Xib0 = PDGID(5232)
Xib_minus = PDGID(5132)
Omegab_minus = PDGID(5332)
