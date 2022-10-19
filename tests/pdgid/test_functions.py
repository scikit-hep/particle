# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from particle.pdgid import (
    A,
    J,
    L,
    S,
    Z,
    charge,
    has_bottom,
    has_charm,
    has_down,
    has_fundamental_anti,
    has_strange,
    has_top,
    has_up,
    is_baryon,
    is_diquark,
    is_dyon,
    is_excited_quark_or_lepton,
    is_gauge_boson_or_higgs,
    is_generator_specific,
    is_hadron,
    is_lepton,
    is_meson,
    is_nucleus,
    is_pentaquark,
    is_Qball,
    is_quark,
    is_Rhadron,
    is_sm_gauge_boson_or_higgs,
    is_sm_lepton,
    is_sm_quark,
    is_special_particle,
    is_SUSY,
    is_technicolor,
    is_valid,
    j_spin,
    l_spin,
    s_spin,
    three_charge,
)


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
    assert charge(PDGIDs.DD1) == -2 / 3
    assert charge(PDGIDs.SD0) == -2 / 3
    assert charge(PDGIDs.Invalid1) is None
    assert charge(PDGIDs.Invalid2) is None


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
    assert three_charge(PDGIDs.Invalid1) is None
    assert three_charge(PDGIDs.Invalid2) is None


def test_is_valid(PDGIDs):
    assert is_valid(PDGIDs.Photon)
    assert is_valid(PDGIDs.Gluon)
    assert is_valid(PDGIDs.Electron)
    assert is_valid(PDGIDs.AntiMuon)
    assert is_valid(PDGIDs.jpsi)
    assert is_valid(PDGIDs.Upsilon_1S)
    assert is_valid(PDGIDs.PiPlus)
    assert is_valid(PDGIDs.KMinus)
    assert is_valid(PDGIDs.D0)
    assert is_valid(PDGIDs.DPlus)
    assert is_valid(PDGIDs.DsPlus)
    assert is_valid(PDGIDs.B0)
    assert is_valid(PDGIDs.Bs)
    assert is_valid(PDGIDs.BcPlus)
    assert is_valid(PDGIDs.Proton)
    assert is_valid(PDGIDs.LcPlus)
    assert is_valid(PDGIDs.Lb)
    assert is_valid(PDGIDs.DD1)
    assert is_valid(PDGIDs.SD0)
    assert not is_valid(PDGIDs.Invalid1)
    assert not is_valid(PDGIDs.Invalid2)


def test_is_quark(PDGIDs):
    _quarks = (
        PDGIDs.DQuark,
        PDGIDs.UQuark,
        PDGIDs.SQuark,
        PDGIDs.CQuark,
        PDGIDs.BQuark,
        PDGIDs.TQuark,
        PDGIDs.BPrimeQuark,
        PDGIDs.TPrimeQuark,
    )
    _non_quarks = [id for id in PDGIDs if id not in _quarks]
    for id in _quarks:
        assert is_quark(id)
    for id in _non_quarks:
        assert not is_quark(id)


def test_is_sm_quark(PDGIDs):
    _sm_quarks = (
        PDGIDs.DQuark,
        PDGIDs.UQuark,
        PDGIDs.SQuark,
        PDGIDs.CQuark,
        PDGIDs.BQuark,
        PDGIDs.TQuark,
    )
    _non_sm_quarks = [id for id in PDGIDs if id not in _sm_quarks]
    for id in _sm_quarks:
        assert is_sm_quark(id)
    for id in _non_sm_quarks:
        assert not is_sm_quark(id)


def test_is_lepton(PDGIDs):
    _leptons = (
        PDGIDs.Electron,
        PDGIDs.Positron,
        PDGIDs.Muon,
        PDGIDs.AntiMuon,
        PDGIDs.Tau,
        PDGIDs.TauPrime,
        PDGIDs.Nu_e,
        PDGIDs.NuBar_tau,
    )
    _non_leptons = [id for id in PDGIDs if id not in _leptons]
    for id in _leptons:
        assert is_lepton(id)
    for id in _non_leptons:
        assert not is_lepton(id)


def test_is_sm_lepton(PDGIDs):
    _sm_leptons = (
        PDGIDs.Electron,
        PDGIDs.Positron,
        PDGIDs.Muon,
        PDGIDs.AntiMuon,
        PDGIDs.Tau,
        PDGIDs.Nu_e,
        PDGIDs.NuBar_tau,
    )
    _non_sm_leptons = [id for id in PDGIDs if id not in _sm_leptons]
    for id in _sm_leptons:
        assert is_sm_lepton(id)
    for id in _non_sm_leptons:
        assert not is_sm_lepton(id)


def test_is_meson(PDGIDs):
    _mesons = (
        PDGIDs.jpsi,
        PDGIDs.psi_2S,
        PDGIDs.Upsilon_1S,
        PDGIDs.Upsilon_4S,
        PDGIDs.Pi0,
        PDGIDs.PiPlus,
        PDGIDs.eta,
        PDGIDs.eta_prime,
        PDGIDs.a_0_1450_plus,
        PDGIDs.KL,
        PDGIDs.KS,
        PDGIDs.KMinus,
        PDGIDs.phi,
        PDGIDs.omega,
        PDGIDs.rho_770_minus,
        PDGIDs.K1_1270_0,
        PDGIDs.K1_1400_0,
        PDGIDs.rho_1700_0,
        PDGIDs.a2_1320_minus,
        PDGIDs.omega_3_1670,
        PDGIDs.f_4_2300,
        PDGIDs.D0,
        PDGIDs.DPlus,
        PDGIDs.DsPlus,
        PDGIDs.B0,
        PDGIDs.BPlus,
        PDGIDs.Bs,
        PDGIDs.BcPlus,
        PDGIDs.Pi0TC,
        PDGIDs.PiMinusTC,
        PDGIDs.T0,
        PDGIDs.Reggeon,
        PDGIDs.Pomeron,
        PDGIDs.Odderon,
        PDGIDs.RPlus_TTildeDbar,
        PDGIDs.R0_GTildeG,
    )
    _non_mesons = [id for id in PDGIDs if id not in _mesons]
    for id in _mesons:
        assert is_meson(id)
    for id in _non_mesons:
        assert not is_meson(id)


def test_is_meson_B_mass_eigenstates():
    # Test special IDs of B(L)0, B(sL)0, B(H)0, B(sH)0
    for pdgid in {150, 350, 510, 530}:
        assert is_meson(pdgid)


def test_is_baryon(PDGIDs):
    _baryons = (
        PDGIDs.Proton,
        PDGIDs.AntiNeutron,
        PDGIDs.HydrogenNucleus,
        PDGIDs.Lambda,
        PDGIDs.Sigma0,
        PDGIDs.SigmaPlus,
        PDGIDs.SigmaMinus,
        PDGIDs.Xi0,
        PDGIDs.AntiXiMinus,
        PDGIDs.OmegaMinus,
        PDGIDs.LcPlus,
        PDGIDs.Lb,
        PDGIDs.LtPlus,
        PDGIDs.RPlusPlus_GTildeUUU,
        PDGIDs.UCbarCUDPentaquark,
        PDGIDs.AntiUCbarCUDPentaquark,
    )
    _non_baryons = [id for id in PDGIDs if id not in _baryons]
    for id in _baryons:
        assert is_baryon(id)
    for id in _non_baryons:
        assert not is_baryon(id)


def test_is_baryon_old_codes_diffractive():
    # Test old codes for diffractive p and n (MC usage)
    assert is_baryon(2110)
    assert is_baryon(2210)


def test_is_hadron(PDGIDs):
    for id in PDGIDs:
        assert is_hadron(id) == (is_meson(id) or is_baryon(id))


def test_is_pentaquark(PDGIDs):
    _pentaquarks = (PDGIDs.UCbarCUDPentaquark, PDGIDs.AntiUCbarCUDPentaquark)
    _non_pentaquarks = [id for id in PDGIDs if id not in _pentaquarks]
    assert is_pentaquark(PDGIDs.UCbarCUDPentaquark)
    assert is_pentaquark(PDGIDs.AntiUCbarCUDPentaquark)
    for id in _non_pentaquarks:
        assert not is_pentaquark(id)


def test_is_gauge_boson_or_higgs(PDGIDs):
    _gb_and_higgs = (
        PDGIDs.Gluon,
        PDGIDs.Photon,
        PDGIDs.Z0,
        PDGIDs.WMinus,
        PDGIDs.HiggsBoson,
        PDGIDs.ZPrime,
        PDGIDs.Graviton,
    )
    _non_gb_and_higgs = [id for id in PDGIDs if id not in _gb_and_higgs]
    for id in _gb_and_higgs:
        assert is_gauge_boson_or_higgs(id)
    for id in _non_gb_and_higgs:
        assert not is_gauge_boson_or_higgs(id)


def test_is_sm_gauge_boson_or_higgs(PDGIDs):
    _sm_gb_and_higgs = (
        PDGIDs.Gluon,
        PDGIDs.Photon,
        PDGIDs.Z0,
        PDGIDs.WMinus,
        PDGIDs.HiggsBoson,
    )
    _non_sm_gb_and_higgs = [id for id in PDGIDs if id not in _sm_gb_and_higgs]
    for id in _sm_gb_and_higgs:
        assert is_sm_gauge_boson_or_higgs(id)
    for id in _non_sm_gb_and_higgs:
        assert not is_sm_gauge_boson_or_higgs(id)


def test_is_generator_specific(PDGIDs):
    _generator_specific = (PDGIDs.AntiCHadron,)
    _non_generator_specific = [id for id in PDGIDs if id not in _generator_specific]
    for id in _generator_specific:
        assert is_generator_specific(id)
    for id in _non_generator_specific:
        assert not is_generator_specific(id)


def test_is_special_particle(PDGIDs):
    _special_particle = (
        PDGIDs.Graviton,
        PDGIDs.Reggeon,
        PDGIDs.Pomeron,
        PDGIDs.Odderon,
        PDGIDs.AntiCHadron,
    )
    _non_special_particle = [id for id in PDGIDs if id not in _special_particle]
    for id in _special_particle:
        assert is_special_particle(id)
    for id in _non_special_particle:
        assert not is_special_particle(id)


def test_is_nucleus(PDGIDs):
    _nuclei = (
        PDGIDs.Proton,
        PDGIDs.AntiNeutron,
        PDGIDs.HydrogenNucleus,
        PDGIDs.Carbon12,
    )
    _non_nuclei = [id for id in PDGIDs if id not in _nuclei]
    for id in _nuclei:
        assert is_nucleus(id)
    for id in _non_nuclei:
        assert not is_nucleus(id)
    # test 10-digit IDs that does not conform with form for nuclei (should start with +/- 10)
    assert not is_nucleus(2000000010)
    assert not is_nucleus(1100000010)


def test_is_diquark(PDGIDs):
    _diquarks = (PDGIDs.DD1, PDGIDs.SD0)
    _non_diquarks = [id for id in PDGIDs if id not in _diquarks]
    for id in _diquarks:
        assert is_diquark(id)
    for id in _non_diquarks:
        assert not is_diquark(id)


def test_is_Rhadron(PDGIDs):
    _Rhadrons = (PDGIDs.RPlus_TTildeDbar, PDGIDs.R0_GTildeG, PDGIDs.RPlusPlus_GTildeUUU)
    _non_Rhadrons = [id for id in PDGIDs if id not in _Rhadrons]
    for id in _Rhadrons:
        assert is_Rhadron(id)
    for id in _non_Rhadrons:
        assert not is_Rhadron(id)


def test_is_Qball(PDGIDs):
    _Qballs = (PDGIDs.QBall1, PDGIDs.QBall2)
    _non_Qballs = [id for id in PDGIDs if id not in _Qballs]
    for id in _Qballs:
        assert is_Qball(id)
    for id in _non_Qballs:
        assert not is_Qball(id)


def test_is_dyon(PDGIDs):
    _dyons = (PDGIDs.DyonSameMagElecChargeSign, PDGIDs.DyonOppositeMagElecChargeSign)
    _non_dyons = [id for id in PDGIDs if id not in _dyons]
    for id in _dyons:
        assert is_dyon(id)
    for id in _non_dyons:
        assert not is_dyon(id)


def test_is_SUSY(PDGIDs):
    _susy = (PDGIDs.Gluino, PDGIDs.Gravitino, PDGIDs.STildeL, PDGIDs.CTildeR)
    _non_susy = [id for id in PDGIDs if id not in _susy]
    for id in _susy:
        assert is_SUSY(id)
    for id in _non_susy:
        assert not is_SUSY(id)


def test_is_technicolor(PDGIDs):
    _technicolor = (PDGIDs.Pi0TC, PDGIDs.PiMinusTC)
    _non_technicolor = [id for id in PDGIDs if id not in _technicolor]
    for id in _technicolor:
        assert is_technicolor(id)
    for id in _non_technicolor:
        assert not is_technicolor(id)


def test_is_excited_quark_or_lepton(PDGIDs):
    _excited_quark_or_lepton = (PDGIDs.UQuarkStar, PDGIDs.AntiElectronStar)
    _non_excited_quark_or_lepton = [
        id for id in PDGIDs if id not in _excited_quark_or_lepton
    ]
    for id in _excited_quark_or_lepton:
        assert is_excited_quark_or_lepton(id)
    for id in _non_excited_quark_or_lepton:
        assert not is_excited_quark_or_lepton(id)


def test_has_down(PDGIDs):
    assert not has_down(PDGIDs.Photon)
    assert not has_down(PDGIDs.Gluon)
    assert not has_down(PDGIDs.Electron)
    assert not has_down(PDGIDs.AntiMuon)
    assert not has_down(PDGIDs.jpsi)
    assert not has_down(PDGIDs.Upsilon_1S)
    assert has_down(PDGIDs.PiPlus)
    assert not has_down(PDGIDs.KMinus)
    assert not has_down(PDGIDs.D0)
    assert has_down(PDGIDs.DPlus)
    assert not has_down(PDGIDs.DsPlus)
    assert has_down(PDGIDs.B0)
    assert not has_down(PDGIDs.Bs)
    assert not has_down(PDGIDs.BcPlus)
    assert has_down(PDGIDs.Proton)
    assert has_down(PDGIDs.LcPlus)
    assert has_down(PDGIDs.Lb)
    assert has_down(PDGIDs.DD1)
    assert has_down(PDGIDs.SD0)
    assert not has_down(PDGIDs.Invalid1)
    assert not has_down(PDGIDs.Invalid2)


def test_has_up(PDGIDs):
    assert not has_up(PDGIDs.Photon)
    assert not has_up(PDGIDs.Gluon)
    assert not has_up(PDGIDs.Electron)
    assert not has_up(PDGIDs.AntiMuon)
    assert not has_up(PDGIDs.jpsi)
    assert not has_up(PDGIDs.Upsilon_1S)
    assert has_up(PDGIDs.PiPlus)
    assert has_up(PDGIDs.KMinus)
    assert has_up(PDGIDs.D0)
    assert not has_up(PDGIDs.DPlus)
    assert not has_up(PDGIDs.DsPlus)
    assert not has_up(PDGIDs.B0)
    assert not has_up(PDGIDs.Bs)
    assert not has_up(PDGIDs.BcPlus)
    assert has_up(PDGIDs.Proton)
    assert has_up(PDGIDs.LcPlus)
    assert has_up(PDGIDs.Lb)
    assert not has_up(PDGIDs.DD1)
    assert not has_up(PDGIDs.SD0)
    assert not has_up(PDGIDs.Invalid1)
    assert not has_up(PDGIDs.Invalid2)


def test_has_strange(PDGIDs):
    assert not has_strange(PDGIDs.Photon)
    assert not has_strange(PDGIDs.Gluon)
    assert not has_strange(PDGIDs.Electron)
    assert not has_strange(PDGIDs.AntiMuon)
    assert not has_strange(PDGIDs.jpsi)
    assert not has_strange(PDGIDs.Upsilon_1S)
    assert not has_strange(PDGIDs.PiPlus)
    assert has_strange(PDGIDs.KMinus)
    assert not has_strange(PDGIDs.D0)
    assert not has_strange(PDGIDs.DPlus)
    assert has_strange(PDGIDs.DsPlus)
    assert not has_strange(PDGIDs.B0)
    assert has_strange(PDGIDs.Bs)
    assert not has_strange(PDGIDs.BcPlus)
    assert not has_strange(PDGIDs.Proton)
    assert not has_strange(PDGIDs.LcPlus)
    assert not has_strange(PDGIDs.Lb)
    assert not has_strange(PDGIDs.DD1)
    assert has_strange(PDGIDs.SD0)
    assert not has_strange(PDGIDs.Invalid1)
    assert not has_strange(PDGIDs.Invalid2)


def test_has_charm(PDGIDs):
    _with_charm_content = (
        PDGIDs.jpsi,
        PDGIDs.psi_2S,
        PDGIDs.D0,
        PDGIDs.DPlus,
        PDGIDs.DsPlus,
        PDGIDs.BcPlus,
        PDGIDs.LcPlus,
        PDGIDs.UCbarCUDPentaquark,
        PDGIDs.AntiUCbarCUDPentaquark,
    )
    _without_charm_content = [id for id in PDGIDs if id not in _with_charm_content]
    for id in _with_charm_content:
        assert has_charm(id)
    for id in _without_charm_content:
        assert not has_charm(id)


def test_has_bottom(PDGIDs):
    _with_bottom_content = (
        PDGIDs.Upsilon_1S,
        PDGIDs.Upsilon_4S,
        PDGIDs.B0,
        PDGIDs.BPlus,
        PDGIDs.Bs,
        PDGIDs.BcPlus,
        PDGIDs.Lb,
    )
    _without_bottom_content = [id for id in PDGIDs if id not in _with_bottom_content]
    for id in _with_bottom_content:
        assert has_bottom(id)
    for id in _without_bottom_content:
        assert not has_bottom(id)


def test_has_top(PDGIDs):
    assert has_top(PDGIDs.T0)
    assert has_top(PDGIDs.LtPlus)
    _no_top = [
        id for id in PDGIDs if id not in (PDGIDs.T0, PDGIDs.LtPlus)
    ]  # top quark should also return has_top(6)==False !
    for id in _no_top:
        assert not has_top(id)


def test_has_fundamental_anti(PDGIDs):
    # Particles that are "fundamental" and not their own antiparticle
    _yep = (
        PDGIDs.WMinus,
        PDGIDs.Electron,
        PDGIDs.Positron,
        PDGIDs.Muon,
        PDGIDs.AntiMuon,
        PDGIDs.Tau,
        PDGIDs.TauPrime,
        PDGIDs.Nu_e,
        PDGIDs.NuBar_tau,
        PDGIDs.DQuark,
        PDGIDs.UQuark,
        PDGIDs.SQuark,
        PDGIDs.CQuark,
        PDGIDs.BQuark,
        PDGIDs.TQuark,
        PDGIDs.BPrimeQuark,
        PDGIDs.TPrimeQuark,
        PDGIDs.UQuarkStar,
        PDGIDs.AntiElectronStar,
        PDGIDs.STildeL,
        PDGIDs.CTildeR,
        PDGIDs.AntiCHadron,
    )
    _nope = [id for id in PDGIDs if id not in _yep]
    for id in _yep:
        assert has_fundamental_anti(id)
    for id in _nope:
        assert not has_fundamental_anti(id)


def mesons_JSL_states_list(PDGIDs, jsl):
    _states = {
        "000": (
            PDGIDs.Pi0,
            PDGIDs.PiPlus,
            PDGIDs.eta,
            PDGIDs.eta_prime,
            PDGIDs.KL,
            PDGIDs.KS,
            PDGIDs.KMinus,
            PDGIDs.D0,
            PDGIDs.DPlus,
            PDGIDs.DsPlus,
            PDGIDs.B0,
            PDGIDs.BPlus,
            PDGIDs.Bs,
            PDGIDs.BcPlus,
            PDGIDs.T0,
        ),
        "011": (PDGIDs.a_0_1450_plus,),
        "101": (PDGIDs.K1_1270_0,),
        "110": (PDGIDs.rho_770_minus,),
        "111": (PDGIDs.K1_1400_0,),
        "112": (PDGIDs.rho_1700_0,),
        # '202': (),
        "211": (PDGIDs.a2_1320_minus,),
        # '212': (),
        # '213': (),
        # '303': (),
        "312": (PDGIDs.omega_3_1670,),
        # '313': (),
        # '314': (),
        # '404': (),
        # '413': (),
        # '414': (),
        # '415': ()
    }
    return _states[jsl]


def test_JSL_mesons(PDGIDs):
    _JSL_eq_000 = mesons_JSL_states_list(PDGIDs, "000")
    _JSL_eq_011 = mesons_JSL_states_list(PDGIDs, "011")
    _JSL_eq_101 = mesons_JSL_states_list(PDGIDs, "101")
    _JSL_eq_110 = mesons_JSL_states_list(PDGIDs, "110")
    _JSL_eq_111 = mesons_JSL_states_list(PDGIDs, "111")
    _JSL_eq_112 = mesons_JSL_states_list(PDGIDs, "112")
    _JSL_eq_211 = mesons_JSL_states_list(PDGIDs, "211")
    _JSL_eq_312 = mesons_JSL_states_list(PDGIDs, "312")

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
    assert s_spin(PDGIDs.f_4_2300) is None
    assert l_spin(PDGIDs.f_4_2300) is None


def test_J_non_mesons(PDGIDs):
    # TODO:  test special particles, supersymmetric particles, R-hadrons, di-quarks, nuclei and pentaquarks
    _J_eq_0 = ()
    _J_eq_1 = (
        PDGIDs.Gluon,
        PDGIDs.Photon,
        PDGIDs.Z0,
        PDGIDs.jpsi,
        PDGIDs.psi_2S,
        PDGIDs.Upsilon_1S,
        PDGIDs.Upsilon_4S,
        PDGIDs.K1_1270_0,
    )
    _J_eq_1over2 = (
        PDGIDs.Electron,
        PDGIDs.Positron,
        PDGIDs.Muon,
        PDGIDs.AntiMuon,
        PDGIDs.Tau,
        PDGIDs.Nu_e,
        PDGIDs.NuBar_tau,
        PDGIDs.DQuark,
        PDGIDs.UQuark,
        PDGIDs.SQuark,
        PDGIDs.CQuark,
        PDGIDs.BQuark,
        PDGIDs.TQuark,
        PDGIDs.Proton,
        PDGIDs.AntiNeutron,
        PDGIDs.Lambda,
        PDGIDs.Sigma0,
        PDGIDs.SigmaPlus,
        PDGIDs.SigmaMinus,
        PDGIDs.Xi0,
        PDGIDs.AntiXiMinus,
        PDGIDs.LcPlus,
        PDGIDs.Lb,
        PDGIDs.LtPlus,
        PDGIDs.STildeL,
        PDGIDs.CTildeR,
    )
    _J_eq_3over2 = (PDGIDs.OmegaMinus,)
    _invalid_pdgids = (PDGIDs.Invalid1, PDGIDs.Invalid2)
    # cases not dealt with in the code, where None is returned
    _J_eq_None = (PDGIDs.TauPrime, PDGIDs.BPrimeQuark, PDGIDs.TPrimeQuark)

    for id in _J_eq_0:
        assert j_spin(id) == 1
    for id in _J_eq_1:
        assert j_spin(id) == 3
    for id in _J_eq_1over2:
        assert j_spin(id) == 2
    for id in _J_eq_3over2:
        assert j_spin(id) == 4
    for id in _invalid_pdgids:
        assert j_spin(id) is None
    for id in _J_eq_None:
        assert j_spin(id) is None


def test_S_non_mesons(PDGIDs):
    _S_eq_None = (PDGIDs.Gluon, PDGIDs.Photon, PDGIDs.Z0)
    for id in _S_eq_None:
        assert S(id) is None


def test_L_non_mesons(PDGIDs):
    _L_eq_None = (PDGIDs.Gluon, PDGIDs.Photon, PDGIDs.Z0)
    for id in _L_eq_None:
        assert L(id) is None


def test_A(PDGIDs):
    _nuclei = {
        PDGIDs.Proton: 1,
        PDGIDs.AntiNeutron: 1,
        PDGIDs.HydrogenNucleus: 1,
        PDGIDs.Carbon12: 12,
    }
    _non_nuclei = [id for id in PDGIDs if id not in _nuclei.keys()]
    for id, a in _nuclei.items():
        assert A(id) == a
    for id in _non_nuclei:
        assert A(id) is None


def test_Z(PDGIDs):
    _nuclei = {
        PDGIDs.Proton: 1,
        PDGIDs.AntiNeutron: 0,
        PDGIDs.HydrogenNucleus: 1,
        PDGIDs.Carbon12: 6,
    }
    _non_nuclei = [id for id in PDGIDs if id not in _nuclei.keys()]
    for id, z in _nuclei.items():
        assert Z(id) == z
    for id in _non_nuclei:
        assert Z(id) is None
