# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import, division, print_function

import pytest

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
from particle.pdgid import has_fundamental_anti
from particle.pdgid import charge
from particle.pdgid import three_charge
from particle.pdgid import J
from particle.pdgid import j_spin
from particle.pdgid import S
from particle.pdgid import s_spin
from particle.pdgid import L
from particle.pdgid import l_spin
from particle.pdgid import P
from particle.pdgid import C
from particle.pdgid import A
from particle.pdgid import Z


def test_charge(PDGIDs):
    assert charge(PDGIDs.Photon) == 0
    assert charge(PDGIDs.Gluon) == 0
    assert charge(PDGIDs.Electron) == -1
    assert charge(PDGIDs.AntiMuon) == +1
    assert charge(PDGIDs.jpsi) == 0
    assert charge(PDGIDs.Upsilon_1S) == 0
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


def test_three_charge(PDGIDs):
    assert three_charge(PDGIDs.Photon) == 0
    assert three_charge(PDGIDs.Electron) == -3
    assert three_charge(PDGIDs.jpsi) == 0
    assert three_charge(PDGIDs.Upsilon_1S) == 0
    assert three_charge(PDGIDs.KMinus) == -3
    assert three_charge(PDGIDs.D0) == 0
    assert three_charge(PDGIDs.Proton) == +3
    assert three_charge(PDGIDs.LcPlus) == +3
    assert three_charge(PDGIDs.Lb) == 0
    assert three_charge(PDGIDs.DD1) == -2
    assert three_charge(PDGIDs.SD0) == -2
    assert three_charge(PDGIDs.Invalid1) == None
    assert three_charge(PDGIDs.Invalid2) == None


def test_is_valid(PDGIDs):
    assert is_valid(PDGIDs.Photon) == True
    assert is_valid(PDGIDs.Gluon) == True
    assert is_valid(PDGIDs.Electron) == True
    assert is_valid(PDGIDs.AntiMuon) == True
    assert is_valid(PDGIDs.jpsi) == True
    assert is_valid(PDGIDs.Upsilon_1S) == True
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


def test_is_lepton(PDGIDs):
    _leptons = (PDGIDs.Electron, PDGIDs.Positron, PDGIDs.Muon, PDGIDs.AntiMuon, PDGIDs.Tau, PDGIDs.TauPrime, PDGIDs.Nu_e, PDGIDs.NuBar_tau)
    _non_leptons = [id for id in PDGIDs if id not in _leptons]
    for id in _leptons: assert is_lepton(id) == True
    for id in _non_leptons: assert is_lepton(id) == False


def test_is_meson(PDGIDs):
    _mesons = (PDGIDs.jpsi, PDGIDs.psi_2S, PDGIDs.Upsilon_1S, PDGIDs.Upsilon_4S,
               PDGIDs.Pi0, PDGIDs.PiPlus, PDGIDs.eta, PDGIDs.eta_prime,
               PDGIDs.a_0_1450_plus, PDGIDs.KL, PDGIDs.KS, PDGIDs.KMinus, PDGIDs.phi, PDGIDs.Omega,
               PDGIDs.rho_770_minus,PDGIDs.K1_1270_0, PDGIDs.K1_1400_0,
               PDGIDs.rho_1700_0,
               PDGIDs.a2_1320_minus,
               PDGIDs.omega_3_1670,
               PDGIDs.f_4_2300,
               PDGIDs.D0, PDGIDs.DPlus, PDGIDs.DsPlus,
               PDGIDs.B0, PDGIDs.BPlus, PDGIDs.Bs, PDGIDs.BcPlus,
               PDGIDs.T0,
               PDGIDs.Reggeon, PDGIDs.Pomeron, PDGIDs.Odderon,
               PDGIDs.RPlus_TTildeDbar, PDGIDs.R0_GTildeG)
    _non_mesons = [id for id in PDGIDs if id not in _mesons]
    for id in _mesons: assert is_meson(id) == True
    for id in _non_mesons: assert is_meson(id) == False


def test_is_baryon(PDGIDs):
    _baryons = (PDGIDs.Proton, PDGIDs.AntiNeutron, PDGIDs.Lambda, PDGIDs.Sigma0, PDGIDs.SigmaPlus, PDGIDs.SigmaMinus, PDGIDs.Xi0,  PDGIDs.AntiXiMinus,PDGIDs.OmegaMinus,
                PDGIDs.LcPlus,
                PDGIDs.Lb,
                PDGIDs.LtPlus,
                PDGIDs.RPlusPlus_GTildeUUU,
                PDGIDs.UCbarCUDPentaquark, PDGIDs.AntiUCbarCUDPentaquark)
    _non_baryons = [id for id in PDGIDs if id not in _baryons]
    for id in _baryons: assert is_baryon(id) == True
    for id in _non_baryons: assert is_baryon(id) == False


def test_is_hadron(PDGIDs):
    for id in PDGIDs:
        assert is_hadron(id) == (is_meson(id) or is_baryon(id))


def test_is_diquark(PDGIDs):
    _diquarks = (PDGIDs.DD1, PDGIDs.SD0)
    _non_diquarks = [id for id in PDGIDs if id not in _diquarks]
    for id in _diquarks: assert is_diquark(id) == True
    for id in _non_diquarks: assert is_diquark(id) == False


def test_is_pentaquark(PDGIDs):
    _pentaquarks = (PDGIDs.UCbarCUDPentaquark, PDGIDs.AntiUCbarCUDPentaquark)
    _non_pentaquarks = [id for id in PDGIDs if id not in _pentaquarks]
    assert is_pentaquark(PDGIDs.UCbarCUDPentaquark) == True
    assert is_pentaquark(PDGIDs.AntiUCbarCUDPentaquark) == True
    for id in _non_pentaquarks: assert is_pentaquark(id) == False


def test_is_nucleus(PDGIDs):
    _nuclei = (PDGIDs.Proton, PDGIDs.HydrogenNucleus, PDGIDs.Carbon12)
    _non_nuclei = [id for id in PDGIDs if id not in _nuclei]
    for id in _nuclei: assert is_nucleus(id) == True
    for id in _non_nuclei: assert is_nucleus(id) == False


def test_is_Rhadron(PDGIDs):
    _Rhadrons = (PDGIDs.RPlus_TTildeDbar, PDGIDs.R0_GTildeG, PDGIDs.RPlusPlus_GTildeUUU)
    _non_Rhadrons = [id for id in PDGIDs if id not in _Rhadrons]
    for id in _Rhadrons: assert is_Rhadron(id) == True
    for id in _non_Rhadrons: assert is_Rhadron(id) == False


def test_is_Qball(PDGIDs):
    _Qballs = (PDGIDs.QBall1, PDGIDs.QBall2)
    _non_Qballs = [id for id in PDGIDs if id not in _Qballs]
    for id in _Qballs: assert is_Qball(id) == True
    for id in _non_Qballs: assert is_Qball(id) == False


def test_is_dyon(PDGIDs):
    _dyons = (PDGIDs.DyonSameMagElecChargeSign, PDGIDs.DyonOppositeMagElecChargeSign)
    _non_dyons = [id for id in PDGIDs if id not in _dyons]
    for id in _dyons: assert is_dyon(id) == True
    for id in _non_dyons: assert is_dyon(id) == False


def test_is_SUSY(PDGIDs):
    _susy = (PDGIDs.Gluino, PDGIDs.Gravitino, PDGIDs.STildeL, PDGIDs.CTildeR)
    _non_susy = [id for id in PDGIDs if id not in _susy]
    for id in _susy: assert is_SUSY(id) == True
    for id in _non_susy: assert is_SUSY(id) == False


def test_has_down(PDGIDs):
    assert has_down(PDGIDs.Photon) == False
    assert has_down(PDGIDs.Gluon) == False
    assert has_down(PDGIDs.Electron) == False
    assert has_down(PDGIDs.AntiMuon) == False
    assert has_down(PDGIDs.jpsi) == False
    assert has_down(PDGIDs.Upsilon_1S) == False
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


def test_has_up(PDGIDs):
    assert has_up(PDGIDs.Photon) == False
    assert has_up(PDGIDs.Gluon) == False
    assert has_up(PDGIDs.Electron) == False
    assert has_up(PDGIDs.AntiMuon) == False
    assert has_up(PDGIDs.jpsi) == False
    assert has_up(PDGIDs.Upsilon_1S) == False
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


def test_has_strange(PDGIDs):
    assert has_strange(PDGIDs.Photon) == False
    assert has_strange(PDGIDs.Gluon) == False
    assert has_strange(PDGIDs.Electron) == False
    assert has_strange(PDGIDs.AntiMuon) == False
    assert has_strange(PDGIDs.jpsi) == False
    assert has_strange(PDGIDs.Upsilon_1S) == False
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


def test_has_charm(PDGIDs):
    _with_charm_content = (PDGIDs.jpsi, PDGIDs.psi_2S,
                           PDGIDs.D0, PDGIDs.DPlus, PDGIDs.DsPlus,
                           PDGIDs.BcPlus,
                           PDGIDs.LcPlus,
                           PDGIDs.UCbarCUDPentaquark, PDGIDs.AntiUCbarCUDPentaquark)
    _without_charm_content = [id for id in PDGIDs if id not in _with_charm_content]
    for id in _with_charm_content: assert has_charm(id) == True
    for id in _without_charm_content: assert has_charm(id) == False


def test_has_bottom(PDGIDs):
    _with_bottom_content = (PDGIDs.Upsilon_1S, PDGIDs.Upsilon_4S,
                            PDGIDs.B0, PDGIDs.BPlus, PDGIDs.Bs, PDGIDs.BcPlus,
                            PDGIDs.Lb)
    _without_bottom_content = [id for id in PDGIDs if id not in _with_bottom_content]
    for id in _with_bottom_content: assert has_bottom(id) == True
    for id in _without_bottom_content: assert has_bottom(id) == False


def test_has_top(PDGIDs):
    assert has_top(PDGIDs.T0) == True
    assert has_top(PDGIDs.LtPlus) == True
    _no_top = [id for id in PDGIDs if id not in (PDGIDs.T0, PDGIDs.LtPlus)]  # top quark should also return has_top(6)==False !
    for id in _no_top: assert has_top(id) == False


def test_has_fundamental_anti(PDGIDs):
    # Particles that are "fundamental" and not their own antiparticle
    _yep = (PDGIDs.WMinus,
            PDGIDs.Electron, PDGIDs.Positron, PDGIDs.Muon, PDGIDs.AntiMuon, PDGIDs.Tau, PDGIDs.TauPrime,
            PDGIDs.Nu_e, PDGIDs.NuBar_tau,
            PDGIDs.DQuark, PDGIDs.UQuark, PDGIDs.SQuark, PDGIDs.CQuark, PDGIDs.BQuark, PDGIDs.TQuark, PDGIDs.BPrimeQuark, PDGIDs.TPrimeQuark,
            PDGIDs.STildeL, PDGIDs.CTildeR,
            PDGIDs.DyonSameMagElecChargeSign, PDGIDs.DyonOppositeMagElecChargeSign)
    _nope = [id for id in PDGIDs if id not in _yep]
    for id in _yep: assert has_fundamental_anti(id) == True
    for id in _nope: assert has_fundamental_anti(id) == False


def mesons_JSL_states_list(PDGIDs, jsl):
        _states = { '000': (PDGIDs.Pi0, PDGIDs.PiPlus, PDGIDs.eta, PDGIDs.eta_prime, PDGIDs.KL, PDGIDs.KS, PDGIDs.KMinus,
                            PDGIDs.D0, PDGIDs.DPlus, PDGIDs.DsPlus,
                            PDGIDs.B0, PDGIDs.BPlus, PDGIDs.Bs, PDGIDs.BcPlus,
                            PDGIDs.T0),
                    '011': (PDGIDs.a_0_1450_plus,),
                    '101': (PDGIDs.K1_1270_0,),
                    '110': (PDGIDs.rho_770_minus,),
                    '111': (PDGIDs.K1_1400_0,),
                    '112': (PDGIDs.rho_1700_0,),
                    #'202': (),
                    '211': (PDGIDs.a2_1320_minus,),
                    #'212': (),
                    #'213': (),
                    #'303': (),
                    '312': (PDGIDs.omega_3_1670,),
                    #'313': (),
                    #'314': (),
                    #'404': (),
                    #'413': (),
                    #'414': (),
                    #'415': ()
                            }
        return _states[jsl]


def test_JSL_mesons(PDGIDs):
    _JSL_eq_000 = mesons_JSL_states_list(PDGIDs, '000')
    _JSL_eq_011 = mesons_JSL_states_list(PDGIDs, '011')
    _JSL_eq_101 = mesons_JSL_states_list(PDGIDs, '101')
    _JSL_eq_110 = mesons_JSL_states_list(PDGIDs, '110')
    _JSL_eq_111 = mesons_JSL_states_list(PDGIDs, '111')
    _JSL_eq_112 = mesons_JSL_states_list(PDGIDs, '112')
    _JSL_eq_211 = mesons_JSL_states_list(PDGIDs, '211')
    _JSL_eq_312 = mesons_JSL_states_list(PDGIDs, '312')

    for id in _JSL_eq_000:
        assert J(id) == 0
        assert S(id) == 0
        assert L(id) == 0
    for id in _JSL_eq_011:
        assert J(id) == 0
        assert S(id) == 1
        assert L(id) == 1
    for id in _JSL_eq_101:
        assert J(id) == 1
        assert S(id) == 0
        assert L(id) == 1
    for id in _JSL_eq_110:
        assert J(id) == 1
        assert S(id) == 1
        assert L(id) == 0
    for id in _JSL_eq_111:
        assert J(id) == 1
        assert S(id) == 1
        assert L(id) == 1
    for id in _JSL_eq_112:
        assert J(id) == 1
        assert S(id) == 1
        assert L(id) == 2
    for id in _JSL_eq_211:
        assert J(id) == 2
        assert S(id) == 1
        assert L(id) == 1
    for id in _JSL_eq_312:
        assert J(id) == 3
        assert S(id) == 1
        assert L(id) == 2


def test_JSL_badly_known_mesons(PDGIDs):
    assert j_spin(PDGIDs.f_4_2300) == 9
    assert s_spin(PDGIDs.f_4_2300) == None
    assert l_spin(PDGIDs.f_4_2300) == None


def test_J_non_mesons(PDGIDs):
    # TODO:  test special particles, supersymmetric particles, R-hadrons, di-quarks, nuclei and pentaquarks
    _J_eq_0 = ()
    _J_eq_1 = (PDGIDs.Gluon, PDGIDs.Photon, PDGIDs.Z0,
               PDGIDs.jpsi, PDGIDs.psi_2S, PDGIDs.Upsilon_1S, PDGIDs.Upsilon_4S,
               PDGIDs.K1_1270_0)
    _J_eq_1over2 = (PDGIDs.Electron, PDGIDs.Positron, PDGIDs.Muon, PDGIDs.AntiMuon, PDGIDs.Tau,
                    PDGIDs.Nu_e, PDGIDs.NuBar_tau,
                    PDGIDs.DQuark, PDGIDs.UQuark, PDGIDs.SQuark, PDGIDs.CQuark, PDGIDs.BQuark, PDGIDs.TQuark,
                    PDGIDs.Proton, PDGIDs.AntiNeutron, PDGIDs.Lambda, PDGIDs.Sigma0, PDGIDs.SigmaPlus, PDGIDs.SigmaMinus, PDGIDs.Xi0, PDGIDs.AntiXiMinus,
                    PDGIDs.LcPlus,
                    PDGIDs.Lb,
                    PDGIDs.LtPlus,
                    PDGIDs.STildeL, PDGIDs.CTildeR)
    _J_eq_3over2 = (PDGIDs.OmegaMinus,)
    _invalid_pdgids = (PDGIDs.Invalid1, PDGIDs.Invalid2)
    # cases not dealt with in the code, where None is returned
    _J_eq_None= (PDGIDs.TauPrime,
                 PDGIDs.BPrimeQuark, PDGIDs.TPrimeQuark)

    for id in _J_eq_0: assert j_spin(id) == 1
    for id in _J_eq_1: assert j_spin(id) == 3
    for id in _J_eq_1over2: assert j_spin(id) == 2
    for id in _J_eq_3over2: assert j_spin(id) == 4
    for id in _invalid_pdgids: assert j_spin(id) == None
    for id in _J_eq_None: assert j_spin(id) == None


def test_S_non_mesons(PDGIDs):
    _S_eq_None= (PDGIDs.Gluon, PDGIDs.Photon, PDGIDs.Z0)
    for id in _S_eq_None: assert S(id) == None


def test_L_non_mesons(PDGIDs):
    _L_eq_None= (PDGIDs.Gluon, PDGIDs.Photon, PDGIDs.Z0)
    for id in _L_eq_None: assert L(id) == None


def test_PC_mesons(PDGIDs):
# List of pairs (P, C) for a list of PDG IDs
    list_PC_pairs = (
        (PDGIDs.Pi0, -1, +1),
        (PDGIDs.PiPlus, -1, None),
        (PDGIDs.eta, -1, +1),
        (PDGIDs.eta_prime, -1, +1),
        (PDGIDs.KL, -1, +1),
        (PDGIDs.KS, -1, +1),
        (PDGIDs.KMinus, -1, None),
        (PDGIDs.D0, -1, +1),
        (PDGIDs.DPlus, -1, None),
        (PDGIDs.DsPlus, -1, None),
        (PDGIDs.B0, -1, +1),
        (PDGIDs.BPlus, -1, None),
        (PDGIDs.Bs, -1, +1),
        (PDGIDs.BcPlus, -1, None),
        (PDGIDs.T0, -1, +1),
        (PDGIDs.a_0_1450_plus, +1, None),
        (PDGIDs.K1_1270_0, +1, -1),
        (PDGIDs.rho_770_minus, -1, None),
        (PDGIDs.K1_1400_0, +1, +1),
        (PDGIDs.K1_1400_0, +1, +1),
        (PDGIDs.rho_1700_0, -1, -1),
        (PDGIDs.a2_1320_minus, +1, None),
        (PDGIDs.omega_3_1670, -1, -1)
        )
    for trio in list_PC_pairs:
        assert P(trio[0]) == trio[1]
        assert C(trio[0]) == trio[2]


def test_PC_badly_known_mesons(PDGIDs):
    assert P(PDGIDs.f_4_2300) == None
    assert C(PDGIDs.f_4_2300) == None


def test_P_non_mesons(PDGIDs):
    _non_mesons = (PDGIDs.Gluon, PDGIDs.Photon, PDGIDs.Z0)
    for id in _non_mesons: assert C(id) == None


def test_C_non_mesons(PDGIDs):
    _non_mesons = (PDGIDs.Gluon, PDGIDs.Photon, PDGIDs.Z0)
    for id in _non_mesons: assert C(id) == None


def test_A(PDGIDs):
    _nuclei = { PDGIDs.Proton: 1,
                PDGIDs.HydrogenNucleus: 1,
                PDGIDs.Carbon12: 12
                }
    _non_nuclei = [ id for id in PDGIDs if id not in _nuclei.keys() ]
    for id, a in _nuclei.items(): assert A(id) == a
    for id in _non_nuclei: assert A(id) == None


def test_Z(PDGIDs):
    _nuclei = { PDGIDs.Proton: 1,
                PDGIDs.HydrogenNucleus: 1,
                PDGIDs.Carbon12: 6
                }
    _non_nuclei = [ id for id in PDGIDs if id not in _nuclei.keys() ]
    for id, z in _nuclei.items(): assert Z(id) == z
    for id in _non_nuclei: assert Z(id) == None
