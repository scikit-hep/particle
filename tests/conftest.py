# Copyright (c) 2018-2023, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

from enum import IntEnum

import pytest


class PDGIDsEnum(IntEnum):
    """Sample of PDGIDs on which to run tests."""

    # Gauge and Higgs bosons
    Gluon = 21
    Photon = 22
    Z0 = 23
    WMinus = -24
    HiggsBoson = 25
    ZPrime = 32
    # Charged leptons
    Electron = 11
    Positron = -Electron
    Muon = 13
    AntiMuon = -Muon
    Tau = 15
    # Neutrinos
    Nu_e = 12
    NuBar_tau = -16
    # Quarks
    DQuark = 1
    UQuark = 2
    SQuark = 3
    CQuark = 4
    BQuark = 5
    TQuark = 6
    # 4th generation quarks and leptons
    TauPrime = 17
    BPrimeQuark = 7
    TPrimeQuark = 8
    # Quarkonia
    jpsi = 443
    psi_2S = 100443
    psi_3770 = 30443
    Upsilon_1S = 553
    Upsilon_4S = 300553
    Upsilon_3_2D = 100557
    h_b_3P = 210553
    # Light hadrons
    Pi0 = 111
    PiPlus = 211
    eta = 221
    eta_prime = 331
    a_0_1450_plus = 10211
    KL = 130
    KS = 310
    KMinus = -321
    rho_770_minus = -213
    rho_10219_plus = 10219  # unknown particle added for testing purposes
    phi = 333
    omega = 223
    K1_1270_0 = 10313
    K1_1400_0 = 20313
    K2_1770_minus = -10325
    K2_1820_0_bar = -20315
    K3_10317_0 = 10317  # unknown particle added for testing purposes
    K3_20317_plus = 20317  # unknown particle added for testing purposes
    K3_30317_0 = 30317  # unknown particle added for testing purposes
    K4_20219_minus = -20219  # unknown particle added for testing purposes
    K4_30329_plus = 30329  # unknown particle added for testing purposes
    rho_1700_0 = 30113
    a2_1320_minus = -215
    omega_3_1670 = 227
    f_2_30225 = 30225  # unknown particle added for testing purposes
    f_4_2050 = 229
    f_4_2300 = 9010229  # example of a not-well-known meson
    Proton = 2212
    AntiNeutron = -2112
    Lambda = 3122
    Sigma0 = 3212
    SigmaPlus = 3222
    SigmaMinus = 3112
    Xi0 = 3322
    AntiXiMinus = -3312
    OmegaMinus = 3334
    N1650Plus = 32212
    N1900BarMinus = -42124
    Lambda1810 = 53122
    # Charm hadrons
    D0 = 421
    DPlus = 411
    DsPlus = 431
    LcPlus = 4122
    # Beauty hadrons
    B0 = 511
    BPlus = 521
    Bs = 531
    BcPlus = 541
    Lb = 5122
    # Top hadrons
    T0 = 621
    LtPlus = 6122
    # Special particles
    Graviton = 39
    Reggeon = 110
    Pomeron = 990
    Odderon = 9990
    # Supersymmetric particles
    Gluino = 1000021
    Gravitino = 1000039
    STildeL = 1000003
    CTildeR = 2000004
    # R-hadrons
    R0_1000017 = 1000017
    RPlus_TTildeDbar = 1000612
    R0_GTildeG = 1000993
    RPlusPlus_GTildeUUU = 1092224
    # Q-balls
    QBall1 = 10000150
    QBall2 = -10000200
    # Dyons
    DyonSameMagElecChargeSign = 4110010
    DyonOppositeMagElecChargeSign = 4120010
    # Di-quarks
    DD1 = 1103
    SD0 = 3101
    # Hidden Valley particles
    HV_gv = 4900021
    # Nuclei
    HydrogenNucleus = 1000010010
    Carbon12 = 1000060120
    # Pentaquarks
    AntiUCbarCUDPentaquark = -9422144
    # example of spin 3/2 u-cbar-c-u-d pentaquark decaying to J/psi proton
    UCbarCUDPentaquark = 9422144
    # Technicolor
    Pi0TC = 3000111
    PiMinusTC = -3000211
    # Excited (composite) quarks and leptons
    UQuarkStar = 4000002
    AntiElectronStar = -4000011
    # Generator specific pseudoparticles or concepts
    AntiCHadron = -84
    GenSpecific910 = 910
    GenSpecific999 = 999
    GenSpecific1910 = 1910
    GenSpecific2910 = 2910
    GenSpecific3910 = 3910
    OpticalPhoton = 20022
    Geantino = 480000000
    # Invalid ID
    Invalid1 = 0  # illegal ID
    Invalid2 = 99999999  # general form is a 7-digit number


@pytest.fixture(scope="session")
def PDGIDs():
    return PDGIDsEnum
