# Licensed under a 3-clause BSD style license, see LICENSE.

import pytest

# Backport needed if Python 2 is used
from enum import IntEnum

from hepparticle.pdgid import charge
from hepparticle.pdgid import three_charge
from hepparticle.pdgid import is_valid
from hepparticle.pdgid import has_down
from hepparticle.pdgid import has_up
from hepparticle.pdgid import has_strange
from hepparticle.pdgid import has_charm
from hepparticle.pdgid import has_bottom
from hepparticle.pdgid import has_top


class PDGIDs(IntEnum):
    """Sample of PDGIDs on which to run tests."""
    # Bosons
    Photon = 22
    Gluon = 21
    WMinus = -24
    Z0 = 23
    HiggsBoson = 25
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
    assert charge(PDGIDs.Photon) == 0
    assert charge(PDGIDs.Gluon) == 0
    assert charge(PDGIDs.Electron) == -1
    assert charge(PDGIDs.AntiMuon) == +1
    assert charge(PDGIDs.JPsi) == 0
    assert charge(PDGIDs.PiPlus) == +1
    assert charge(PDGIDs.KMinus) == -1
    assert charge(PDGIDs.B0) == 0
    assert charge(PDGIDs.Bs) == 0
    assert charge(PDGIDs.BcPlus) == +1
    assert charge(PDGIDs.Proton) == +1
    assert charge(PDGIDs.LcPlus) == +1
    assert charge(PDGIDs.Lb) == 0
    assert charge(PDGIDs.Invalid1) == None
    assert charge(PDGIDs.Invalid2) == None
    assert three_charge(PDGIDs.Photon) == 0
    assert three_charge(PDGIDs.Electron) == -3
    assert three_charge(PDGIDs.Proton) == +3
    assert three_charge(PDGIDs.KMinus) == -3
    assert three_charge(PDGIDs.Invalid1) == None
    assert three_charge(PDGIDs.Invalid2) == None


def test_is_valid():
    assert is_valid(PDGIDs.Photon) == True
    assert is_valid(PDGIDs.Gluon) == True
    assert is_valid(PDGIDs.Electron) == True
    assert is_valid(PDGIDs.AntiMuon) == True
    assert is_valid(PDGIDs.JPsi) == True
    assert is_valid(PDGIDs.PiPlus) == True
    assert is_valid(PDGIDs.KMinus) == True
    assert is_valid(PDGIDs.B0) == True
    assert is_valid(PDGIDs.Bs) == True
    assert is_valid(PDGIDs.BcPlus) == True
    assert is_valid(PDGIDs.Proton) == True
    assert is_valid(PDGIDs.Invalid1) == False
    assert is_valid(PDGIDs.Invalid2) == False

def test_has_functions():
    assert has_down(PDGIDs.Photon) == False
    assert has_down(PDGIDs.Gluon) == False
    assert has_down(PDGIDs.Electron) == False
    assert has_down(PDGIDs.AntiMuon) == False
    assert has_down(PDGIDs.JPsi) == False
    assert has_down(PDGIDs.PiPlus) == True
    assert has_down(PDGIDs.KMinus) == False
    assert has_down(PDGIDs.B0) == True
    assert has_down(PDGIDs.Bs) == False
    assert has_down(PDGIDs.BcPlus) == False
    assert has_down(PDGIDs.Proton) == True
    assert has_down(PDGIDs.Invalid1) == False
    assert has_down(PDGIDs.Invalid2) == False
    assert has_down(PDGIDs.Invalid1) == False
    #
    assert has_up(PDGIDs.Photon) == False
    assert has_up(PDGIDs.Gluon) == False
    assert has_up(PDGIDs.Electron) == False
    assert has_up(PDGIDs.AntiMuon) == False
    assert has_up(PDGIDs.JPsi) == False
    assert has_up(PDGIDs.PiPlus) == True
    assert has_up(PDGIDs.KMinus) == True
    assert has_up(PDGIDs.B0) == False
    assert has_up(PDGIDs.Bs) == False
    assert has_up(PDGIDs.BcPlus) == False
    assert has_up(PDGIDs.Proton) == True
    assert has_up(PDGIDs.Invalid1) == False
    assert has_up(PDGIDs.Invalid2) == False
    #
    assert has_strange(PDGIDs.Photon) == False
    assert has_strange(PDGIDs.Gluon) == False
    assert has_strange(PDGIDs.Electron) == False
    assert has_strange(PDGIDs.AntiMuon) == False
    assert has_strange(PDGIDs.JPsi) == False
    assert has_strange(PDGIDs.PiPlus) == False
    assert has_strange(PDGIDs.KMinus) == True
    assert has_strange(PDGIDs.B0) == False
    assert has_strange(PDGIDs.Bs) == True
    assert has_strange(PDGIDs.BcPlus) == False
    assert has_strange(PDGIDs.Proton) == False
    assert has_strange(PDGIDs.Invalid1) == False
    assert has_strange(PDGIDs.Invalid2) == False
    #
    assert has_charm(PDGIDs.Photon) == False
    assert has_charm(PDGIDs.Gluon) == False
    assert has_charm(PDGIDs.Electron) == False
    assert has_charm(PDGIDs.AntiMuon) == False
    assert has_charm(PDGIDs.JPsi) == True
    assert has_charm(PDGIDs.PiPlus) == False
    assert has_charm(PDGIDs.KMinus) == False
    assert has_charm(PDGIDs.B0) == False
    assert has_charm(PDGIDs.Bs) == False
    assert has_charm(PDGIDs.BcPlus) == True
    assert has_charm(PDGIDs.Proton) == False
    assert has_charm(PDGIDs.Invalid1) == False
    assert has_charm(PDGIDs.Invalid2) == False
    #
    assert has_bottom(PDGIDs.Photon) == False
    assert has_bottom(PDGIDs.Gluon) == False
    assert has_bottom(PDGIDs.Electron) == False
    assert has_bottom(PDGIDs.AntiMuon) == False
    assert has_bottom(PDGIDs.JPsi) == False
    assert has_bottom(PDGIDs.PiPlus) == False
    assert has_bottom(PDGIDs.KMinus) == False
    assert has_bottom(PDGIDs.B0) == True
    assert has_bottom(PDGIDs.Bs) == True
    assert has_bottom(PDGIDs.BcPlus) == True
    assert has_bottom(PDGIDs.Proton) == False
    assert has_bottom(PDGIDs.Invalid1) == False
    assert has_bottom(PDGIDs.Invalid2) == False
    #
    assert has_top(PDGIDs.Photon) == False
    assert has_top(PDGIDs.Gluon) == False
    assert has_top(PDGIDs.Electron) == False
    assert has_top(PDGIDs.AntiMuon) == False
    assert has_top(PDGIDs.JPsi) == False
    assert has_top(PDGIDs.PiPlus) == False
    assert has_top(PDGIDs.KMinus) == False
    assert has_top(PDGIDs.B0) == False
    assert has_top(PDGIDs.Bs) == False
    assert has_top(PDGIDs.BcPlus) == False
    assert has_top(PDGIDs.Proton) == False
    assert has_top(PDGIDs.Invalid1) == False
    assert has_top(PDGIDs.Invalid2) == False
