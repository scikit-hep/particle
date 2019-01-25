# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import division

import pytest

from particle.pdgid import charge
from particle.pdgid import three_charge
from particle.pdgid import is_valid
from particle.pdgid import is_lepton
from particle.pdgid import is_hadron
from particle.pdgid import is_meson
from particle.pdgid import is_baryon
from particle.pdgid import is_diquark
from particle.pdgid import is_nucleus
from particle.pdgid import is_pentaquark
from particle.pdgid import is_Rhadron
from particle.pdgid import is_Qball
from particle.pdgid import is_dyon
from particle.pdgid import is_SUSY
from particle.pdgid import has_down
from particle.pdgid import has_up
from particle.pdgid import has_strange
from particle.pdgid import has_charm
from particle.pdgid import has_bottom
from particle.pdgid import has_top


def test_charge_functions(PDGIDs):
    assert charge(PDGIDs.Photon) == 0
    assert charge(PDGIDs.Gluon) == 0
    assert charge(PDGIDs.Electron) == -1
    assert charge(PDGIDs.AntiMuon) == +1
    assert charge(PDGIDs.JPsi) == 0
    assert charge(PDGIDs.Upsilon1S) == 0
    assert charge(PDGIDs.PiPlus) == +1
    assert charge(PDGIDs.KMinus) == -1
    assert charge(PDGIDs.D0) == 0
    assert charge(PDGIDs.DPlus) == +1
    assert charge(PDGIDs.DsPlus) == +1
    assert charge(PDGIDs.B0) == 0
    assert charge(PDGIDs.Bs) == 0
    assert charge(PDGIDs.BcPlus) == +1
    assert charge(PDGIDs.Proton) == +1
    assert charge(PDGIDs.LcPlus) == +1
    assert charge(PDGIDs.Lb) == 0
    assert charge(PDGIDs.DD1) == -2/3
    assert charge(PDGIDs.SD0) == -2/3
    assert charge(PDGIDs.Invalid1) == None
    assert charge(PDGIDs.Invalid2) == None
    assert three_charge(PDGIDs.Photon) == 0
    assert three_charge(PDGIDs.Electron) == -3
    assert three_charge(PDGIDs.JPsi) == 0
    assert three_charge(PDGIDs.Upsilon1S) == 0
    assert three_charge(PDGIDs.KMinus) == -3
    assert three_charge(PDGIDs.D0) == 0
    assert three_charge(PDGIDs.Proton) == +3
    assert three_charge(PDGIDs.LcPlus) == +3
    assert three_charge(PDGIDs.Lb) == 0
    assert three_charge(PDGIDs.DD1) == -2
    assert three_charge(PDGIDs.SD0) == -2
    assert three_charge(PDGIDs.Invalid1) == None
    assert three_charge(PDGIDs.Invalid2) == None


def test_is_functions(PDGIDs):
    assert is_valid(PDGIDs.Photon) == True
    assert is_valid(PDGIDs.Gluon) == True
    assert is_valid(PDGIDs.Electron) == True
    assert is_valid(PDGIDs.AntiMuon) == True
    assert is_valid(PDGIDs.JPsi) == True
    assert is_valid(PDGIDs.Upsilon1S) == True
    assert is_valid(PDGIDs.PiPlus) == True
    assert is_valid(PDGIDs.KMinus) == True
    assert is_valid(PDGIDs.D0) == True
    assert is_valid(PDGIDs.DPlus) == True
    assert is_valid(PDGIDs.DsPlus) == True
    assert is_valid(PDGIDs.B0) == True
    assert is_valid(PDGIDs.Bs) == True
    assert is_valid(PDGIDs.BcPlus) == True
    assert is_valid(PDGIDs.Proton) == True
    assert is_valid(PDGIDs.LcPlus) == True
    assert is_valid(PDGIDs.Lb) == True
    assert is_valid(PDGIDs.DD1) == True
    assert is_valid(PDGIDs.SD0) == True
    assert is_valid(PDGIDs.Invalid1) == False
    assert is_valid(PDGIDs.Invalid2) == False
    #
    _leptons = (PDGIDs.Electron, PDGIDs.Positron, PDGIDs.Muon, PDGIDs.AntiMuon, PDGIDs.Tau, PDGIDs.TauPrime, PDGIDs.Nu_e, PDGIDs.NuBar_tau)
    _non_leptons = [ id for id in PDGIDs if id not in _leptons ]
    for id in _leptons: assert is_lepton(id) == True
    for id in _non_leptons: assert is_lepton(id) == False
    #
    _mesons = (PDGIDs.JPsi, PDGIDs.Psi2S, PDGIDs.Upsilon1S, PDGIDs.Upsilon4S,
               PDGIDs.Pi0, PDGIDs.PiPlus, PDGIDs.A0Plus980, PDGIDs.KL, PDGIDs.KS, PDGIDs.KMinus, PDGIDs.phi, PDGIDs.Omega,
               PDGIDs.D0, PDGIDs.DPlus, PDGIDs.DsPlus,
               PDGIDs.B0, PDGIDs.BPlus, PDGIDs.Bs, PDGIDs.BcPlus,
               PDGIDs.T0,
               PDGIDs.Reggeon, PDGIDs.Pomeron, PDGIDs.Odderon,
               PDGIDs.R0_GTildeG)
    _non_mesons = [ id for id in PDGIDs if id not in _mesons ]
    for id in _mesons: assert is_meson(id) == True
    for id in _non_mesons: assert is_meson(id) == False
    #
    #
    _baryons = (PDGIDs.Proton, PDGIDs.AntiNeutron, PDGIDs.Lambda, PDGIDs.Sigma0, PDGIDs.SigmaPlus, PDGIDs.SigmaMinus, PDGIDs.Xi0,  PDGIDs.XiPlus,PDGIDs.OmegaMinus,
                PDGIDs.LcPlus,
                PDGIDs.Lb,
                PDGIDs.LtPlus,
                PDGIDs.RPlusPlus_GTildeUUU)
    _non_baryons = [ id for id in PDGIDs if id not in _baryons ]
    for id in _baryons: assert is_baryon(id) == True
    for id in _non_baryons: assert is_baryon(id) == False
    #
    for id in PDGIDs:
        assert is_hadron(id) == ( is_meson(id) or is_baryon(id) )
    #
    _diquarks = (PDGIDs.DD1, PDGIDs.SD0)
    _non_diquarks = [ id for id in PDGIDs if id not in _diquarks ]
    for id in _diquarks: assert is_diquark(id) == True
    for id in _non_diquarks: assert is_diquark(id) == False
    #
    for id in PDGIDs: assert is_pentaquark(id) == False
    #
    assert is_nucleus(PDGIDs.Proton) == True
    assert is_nucleus(PDGIDs.HydrogenNucleus) == True
    #
    _Rhadrons = (PDGIDs.R0_GTildeG, PDGIDs.RPlusPlus_GTildeUUU)
    _non_Rhadrons = [ id for id in PDGIDs if id not in _Rhadrons ]
    for id in _Rhadrons: assert is_Rhadron(id) == True
    for id in _non_Rhadrons: assert is_Rhadron(id) == False
    #
    _susy = (PDGIDs.Gluino, PDGIDs.Gravitino, PDGIDs.STildeL, PDGIDs.CTildeR)
    _non_susy = [ id for id in PDGIDs if id not in _susy ]
    for id in _susy: assert is_SUSY(id) == True
    for id in _non_susy: assert is_SUSY(id) == False

def test_has_functions(PDGIDs):
    assert has_down(PDGIDs.Photon) == False
    assert has_down(PDGIDs.Gluon) == False
    assert has_down(PDGIDs.Electron) == False
    assert has_down(PDGIDs.AntiMuon) == False
    assert has_down(PDGIDs.JPsi) == False
    assert has_down(PDGIDs.Upsilon1S) == False
    assert has_down(PDGIDs.PiPlus) == True
    assert has_down(PDGIDs.KMinus) == False
    assert has_down(PDGIDs.D0) == False
    assert has_down(PDGIDs.DPlus) == True
    assert has_down(PDGIDs.DsPlus) == False
    assert has_down(PDGIDs.B0) == True
    assert has_down(PDGIDs.Bs) == False
    assert has_down(PDGIDs.BcPlus) == False
    assert has_down(PDGIDs.Proton) == True
    assert has_down(PDGIDs.LcPlus) == True
    assert has_down(PDGIDs.Lb) == True
    assert has_down(PDGIDs.DD1) == True
    assert has_down(PDGIDs.SD0) == True
    assert has_down(PDGIDs.Invalid1) == False
    assert has_down(PDGIDs.Invalid2) == False
    #
    assert has_up(PDGIDs.Photon) == False
    assert has_up(PDGIDs.Gluon) == False
    assert has_up(PDGIDs.Electron) == False
    assert has_up(PDGIDs.AntiMuon) == False
    assert has_up(PDGIDs.JPsi) == False
    assert has_up(PDGIDs.Upsilon1S) == False
    assert has_up(PDGIDs.PiPlus) == True
    assert has_up(PDGIDs.KMinus) == True
    assert has_up(PDGIDs.D0) == True
    assert has_up(PDGIDs.DPlus) == False
    assert has_up(PDGIDs.DsPlus) == False
    assert has_up(PDGIDs.B0) == False
    assert has_up(PDGIDs.Bs) == False
    assert has_up(PDGIDs.BcPlus) == False
    assert has_up(PDGIDs.Proton) == True
    assert has_up(PDGIDs.LcPlus) == True
    assert has_up(PDGIDs.Lb) == True
    assert has_up(PDGIDs.DD1) == False
    assert has_up(PDGIDs.SD0) == False
    assert has_up(PDGIDs.Invalid1) == False
    assert has_up(PDGIDs.Invalid2) == False
    #
    assert has_strange(PDGIDs.Photon) == False
    assert has_strange(PDGIDs.Gluon) == False
    assert has_strange(PDGIDs.Electron) == False
    assert has_strange(PDGIDs.AntiMuon) == False
    assert has_strange(PDGIDs.JPsi) == False
    assert has_strange(PDGIDs.Upsilon1S) == False
    assert has_strange(PDGIDs.PiPlus) == False
    assert has_strange(PDGIDs.KMinus) == True
    assert has_strange(PDGIDs.D0) == False
    assert has_strange(PDGIDs.DPlus) == False
    assert has_strange(PDGIDs.DsPlus) == True
    assert has_strange(PDGIDs.B0) == False
    assert has_strange(PDGIDs.Bs) == True
    assert has_strange(PDGIDs.BcPlus) == False
    assert has_strange(PDGIDs.Proton) == False
    assert has_strange(PDGIDs.LcPlus) == False
    assert has_strange(PDGIDs.Lb) == False
    assert has_strange(PDGIDs.DD1) == False
    assert has_strange(PDGIDs.SD0) == True
    assert has_strange(PDGIDs.Invalid1) == False
    assert has_strange(PDGIDs.Invalid2) == False
    #
    assert has_charm(PDGIDs.Photon) == False
    assert has_charm(PDGIDs.Gluon) == False
    assert has_charm(PDGIDs.Electron) == False
    assert has_charm(PDGIDs.AntiMuon) == False
    assert has_charm(PDGIDs.JPsi) == True
    assert has_charm(PDGIDs.Upsilon1S) == False
    assert has_charm(PDGIDs.PiPlus) == False
    assert has_charm(PDGIDs.KMinus) == False
    assert has_charm(PDGIDs.D0) == True
    assert has_charm(PDGIDs.DPlus) == True
    assert has_charm(PDGIDs.DsPlus) == True
    assert has_charm(PDGIDs.B0) == False
    assert has_charm(PDGIDs.Bs) == False
    assert has_charm(PDGIDs.BcPlus) == True
    assert has_charm(PDGIDs.Proton) == False
    assert has_charm(PDGIDs.LcPlus) == True
    assert has_charm(PDGIDs.Lb) == False
    assert has_charm(PDGIDs.DD1) == False
    assert has_charm(PDGIDs.SD0) == False
    assert has_charm(PDGIDs.Invalid1) == False
    assert has_charm(PDGIDs.Invalid2) == False
    #
    assert has_bottom(PDGIDs.Photon) == False
    assert has_bottom(PDGIDs.Gluon) == False
    assert has_bottom(PDGIDs.Electron) == False
    assert has_bottom(PDGIDs.AntiMuon) == False
    assert has_bottom(PDGIDs.JPsi) == False
    assert has_bottom(PDGIDs.Upsilon1S) == True
    assert has_bottom(PDGIDs.PiPlus) == False
    assert has_bottom(PDGIDs.KMinus) == False
    assert has_bottom(PDGIDs.D0) == False
    assert has_bottom(PDGIDs.DPlus) == False
    assert has_bottom(PDGIDs.DsPlus) == False
    assert has_bottom(PDGIDs.B0) == True
    assert has_bottom(PDGIDs.Bs) == True
    assert has_bottom(PDGIDs.BcPlus) == True
    assert has_bottom(PDGIDs.Proton) == False
    assert has_bottom(PDGIDs.LcPlus) == False
    assert has_bottom(PDGIDs.Lb) == True
    assert has_bottom(PDGIDs.DD1) == False
    assert has_bottom(PDGIDs.SD0) == False
    assert has_bottom(PDGIDs.Invalid1) == False
    assert has_bottom(PDGIDs.Invalid2) == False
    #
    assert has_top(PDGIDs.T0) == True
    assert has_top(PDGIDs.LtPlus) == True
    _no_top = [ id for id in PDGIDs if id not in (PDGIDs.T0, PDGIDs.LtPlus) ]  # top quark should also return has_top(6)==False !
    for id in _no_top: assert has_top(id) == False
