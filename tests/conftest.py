# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest

# Backport needed if Python 2 is used
from enum import IntEnum


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
    TauPrime = 17
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
    BPrimeQuark = 7  # 4th generation
    TPrimeQuark = 8
    # Quarkonia
    jpsi = 443
    psi_2S = 100443
    Upsilon_1S = 553
    Upsilon_4S = 300553
    # Light hadrons
    Pi0 = 111
    PiPlus = 211
    eta=221
    eta_prime=331
    a_0_1450_plus = 10211
    KL = 130
    KS = 310
    KMinus = -321
    rho_770_minus = -213
    phi = 333
    Omega = 223
    K1_1270_0 = 10313
    K1_1400_0 = 20313
    rho_1700_0 = 30113
    a2_1320_minus = -215
    omega_3_1670 = 227
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
    # Nuclei
    HydrogenNucleus = 1000010010
    Carbon12 = 1000060120
    # Pentaquarks
    UCbarCUDPentaquark = 9422144  # example of spin 3/2 u-cbar-c-u-d pentaquark decaying to J/psi proton
    AntiUCbarCUDPentaquark = -9422144
    # Invalid ID
    Invalid1 = 0  # illegal ID
    Invalid2 = 99999999  # general form is a 7-digit number


@pytest.fixture(scope='session')
def PDGIDs():
    return PDGIDsEnum
