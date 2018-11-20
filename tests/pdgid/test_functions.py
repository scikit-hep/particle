# Licensed under a 3-clause BSD style license, see LICENSE.

import pytest

# Backport needed if Python 2 is used
from enum import IntEnum

from hepparticle.pdgid import charge
from hepparticle.pdgid import three_charge
from hepparticle.pdgid import is_valid


class PDGIDs(IntEnum):
    """Sample of PDGIDs on which to run tests."""
    # Leptons
    Electron = 11
    Positron = -Electron
    Muon = 13
    AntiMuon = -Muon
    Tau = 15
    AntiTau = -Tau
    # Neutrinos
    Nu_e = 12
    NuBar_tau = -16
    # Bosons
    Photon = 22
    Gluon = 21
    WMinus = -24
    Z0 = 23
    HiggsBoson = 25
    # Quarks
    DQuark = 1
    UQuark = 2
    SQuark = 3
    CQuark = 4
    BQuark = 5
    TQuark = 6
    # Quarkonia
    JPsi = 443
    Psi2S = 100443
    Upsilon1S = 553
    Upsilon4S = 300553
    # Light hadrons
    Pi0 = 111
    PiPlus = 211
    KL = 130
    KS = 310
    KMinus = -321
    phi = 333
    Omega = 223
    Proton = 2212
    AntiNeutron = -2112
    Lambda = 3122
    Sigma0 = 3212
    SigmaPlus = 3222
    SigmaMinus = 3112
    Xi0 = 3322
    XiPlus = -3312
    Omegaminus = 3334
    # Charm hadrons
    D0 = 421
    DPlus = 411
    DsPlus = 431
    LcPlus = 4122
    AntiOmega_ccc = -4444
    # Beauty hadrons
    B0 = 511
    BPlus = 521
    Bs = 531
    BcPlus = 541
    LcPlus = 4122
    Lb = 5122
    # Exotic particles
    Reggeon = 110
    Pomeron = 990
    Odderon = 9990
    Graviton = 39
    Gravitino = 1000039
    Gluino = 1000021
    # Di-quarks
    DD1 = 1103
    SD0 = 3101
    # Invalid ID
    Invalid1 = 0  # illegal ID
    Invalid2 = 99999999  # general form is a 7-digit number


def test_charge_functions():
    assert charge(PDGIDs.Gluon) == 0
    assert charge(PDGIDs.Photon) == 0
    assert charge(PDGIDs.Electron) == -1
    assert charge(PDGIDs.PiPlus) == +1
    assert charge(PDGIDs.KMinus) == -1
    assert charge(PDGIDs.Proton) == +1
    assert three_charge(PDGIDs.Photon) == 0
    assert three_charge(PDGIDs.Electron) == -3
    assert three_charge(PDGIDs.Proton) == +3
    assert three_charge(PDGIDs.KMinus) == -3


def test_is_valid():
    assert is_valid(PDGIDs.Gluon) == True
    assert is_valid(PDGIDs.Photon) == True
    assert is_valid(PDGIDs.Electron) == True
    assert is_valid(PDGIDs.PiPlus) == True
    assert is_valid(PDGIDs.Proton) == True
    assert is_valid(PDGIDs.Invalid1) == False
    assert is_valid(PDGIDs.Invalid2) == False
