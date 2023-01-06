# Copyright (c) 2018-2023, Eduardo Rodrigues and Henry Schreiner.
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
    assert three_charge(PDGIDs.R0_1000017) == 0
    assert three_charge(PDGIDs.Invalid1) is None
    assert three_charge(PDGIDs.Invalid2) is None
    assert three_charge(5100061) == 6  # special particle, see three_charge


def test_is_valid(PDGIDs):
    _invalid = (
        PDGIDs.Invalid1,
        PDGIDs.Invalid2,
    )
    _valid = [i for i in PDGIDs if i not in _invalid]
    for i in _valid:
        assert is_valid(i)
    for i in _invalid:
        assert not is_valid(i)


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
    _non_quarks = [pid for pid in PDGIDs if pid not in _quarks]
    for pid in _quarks:
        assert is_quark(pid)
    for pid in _non_quarks:
        assert not is_quark(pid)


def test_is_sm_quark(PDGIDs):
    _sm_quarks = (
        PDGIDs.DQuark,
        PDGIDs.UQuark,
        PDGIDs.SQuark,
        PDGIDs.CQuark,
        PDGIDs.BQuark,
        PDGIDs.TQuark,
    )
    _non_sm_quarks = [pid for pid in PDGIDs if pid not in _sm_quarks]
    for pid in _sm_quarks:
        assert is_sm_quark(pid)
    for pid in _non_sm_quarks:
        assert not is_sm_quark(pid)


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
    _non_leptons = [pid for pid in PDGIDs if pid not in _leptons]
    for pid in _leptons:
        assert is_lepton(pid)
    for pid in _non_leptons:
        assert not is_lepton(pid)


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
    _non_sm_leptons = [pid for pid in PDGIDs if pid not in _sm_leptons]
    for pid in _sm_leptons:
        assert is_sm_lepton(pid)
    for pid in _non_sm_leptons:
        assert not is_sm_lepton(pid)


def _get_mesons(PDGIDs):
    """Trivial helper to collect and return all mesons."""
    _mesons = (
        PDGIDs.jpsi,
        PDGIDs.psi_2S,
        PDGIDs.psi_3770,
        PDGIDs.Upsilon_1S,
        PDGIDs.Upsilon_4S,
        PDGIDs.Upsilon_3_2D,
        PDGIDs.h_b_3P,
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
        PDGIDs.rho_10219_plus,
        PDGIDs.K1_1270_0,
        PDGIDs.K1_1400_0,
        PDGIDs.K2_1770_minus,
        PDGIDs.K2_1820_0_bar,
        PDGIDs.K3_10317_0,
        PDGIDs.K3_20317_plus,
        PDGIDs.K3_30317_0,
        PDGIDs.K4_20219_minus,
        PDGIDs.K4_30329_plus,
        PDGIDs.rho_1700_0,
        PDGIDs.a2_1320_minus,
        PDGIDs.omega_3_1670,
        PDGIDs.f_2_30225,
        PDGIDs.f_4_2050,
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
    return _mesons


def _get_non_mesons(PDGIDs):
    """Trivial helper to collect and return all non-mesons."""
    return [pid for pid in PDGIDs if pid not in _get_mesons(PDGIDs)]


def test_is_meson(PDGIDs):
    for pid in _get_mesons(PDGIDs):
        assert is_meson(pid)
    for pid in _get_non_mesons(PDGIDs):
        assert not is_meson(pid)


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
        PDGIDs.N1650Plus,
        PDGIDs.N1900BarMinus,
        PDGIDs.Lambda1810,
        PDGIDs.LcPlus,
        PDGIDs.Lb,
        PDGIDs.LtPlus,
        PDGIDs.RPlusPlus_GTildeUUU,
        PDGIDs.UCbarCUDPentaquark,
        PDGIDs.AntiUCbarCUDPentaquark,
    )
    _non_baryons = [pid for pid in PDGIDs if pid not in _baryons]
    for pid in _baryons:
        assert is_baryon(pid)
    for pid in _non_baryons:
        assert not is_baryon(pid)


def test_is_baryon_old_codes_diffractive():
    # Test old codes for diffractive p and n (MC usage)
    assert is_baryon(2110)
    assert is_baryon(2210)


def test_is_hadron(PDGIDs):
    for pid in PDGIDs:
        assert is_hadron(pid) == (is_meson(pid) or is_baryon(pid))


def test_is_pentaquark(PDGIDs):
    _pentaquarks = (PDGIDs.UCbarCUDPentaquark, PDGIDs.AntiUCbarCUDPentaquark)
    _non_pentaquarks = [pid for pid in PDGIDs if pid not in _pentaquarks]
    assert is_pentaquark(PDGIDs.UCbarCUDPentaquark)
    assert is_pentaquark(PDGIDs.AntiUCbarCUDPentaquark)
    for pid in _non_pentaquarks:
        assert not is_pentaquark(pid)


def test_pentaquarks_are_baryons(PDGIDs):
    """Obviously all pentaquarks are baryons!"""
    _pentaquarks = (PDGIDs.UCbarCUDPentaquark, PDGIDs.AntiUCbarCUDPentaquark)
    for pid in _pentaquarks:
        assert is_baryon(pid)


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
    _non_gb_and_higgs = [pid for pid in PDGIDs if pid not in _gb_and_higgs]
    for pid in _gb_and_higgs:
        assert is_gauge_boson_or_higgs(pid)
    for pid in _non_gb_and_higgs:
        assert not is_gauge_boson_or_higgs(pid)


def test_is_sm_gauge_boson_or_higgs(PDGIDs):
    _sm_gb_and_higgs = (
        PDGIDs.Gluon,
        PDGIDs.Photon,
        PDGIDs.Z0,
        PDGIDs.WMinus,
        PDGIDs.HiggsBoson,
    )
    _non_sm_gb_and_higgs = [pid for pid in PDGIDs if pid not in _sm_gb_and_higgs]
    for pid in _sm_gb_and_higgs:
        assert is_sm_gauge_boson_or_higgs(pid)
    for pid in _non_sm_gb_and_higgs:
        assert not is_sm_gauge_boson_or_higgs(pid)


def test_is_generator_specific(PDGIDs):
    _generator_specific = (
        PDGIDs.AntiCHadron,
        PDGIDs.GenSpecific910,
        PDGIDs.GenSpecific999,
        PDGIDs.GenSpecific1910,
        PDGIDs.GenSpecific2910,
        PDGIDs.GenSpecific3910,
        PDGIDs.OpticalPhoton,
        PDGIDs.Geantino,
    )
    _non_generator_specific = [pid for pid in PDGIDs if pid not in _generator_specific]
    for pid in _generator_specific:
        assert is_generator_specific(pid)
    for pid in _non_generator_specific:
        assert not is_generator_specific(pid)


def test_is_special_particle(PDGIDs):
    _special_particle = (
        PDGIDs.Graviton,
        PDGIDs.Reggeon,
        PDGIDs.Pomeron,
        PDGIDs.Odderon,
        PDGIDs.AntiCHadron,
        PDGIDs.GenSpecific910,
        PDGIDs.GenSpecific999,
        PDGIDs.GenSpecific1910,
        PDGIDs.GenSpecific2910,
        PDGIDs.GenSpecific3910,
        PDGIDs.OpticalPhoton,
        PDGIDs.Geantino,
    )
    _non_special_particle = [pid for pid in PDGIDs if pid not in _special_particle]
    for pid in _special_particle:
        assert is_special_particle(pid)
    for pid in _non_special_particle:
        assert not is_special_particle(pid)


def test_is_nucleus(PDGIDs):
    _nuclei = (
        PDGIDs.Proton,
        PDGIDs.AntiNeutron,
        PDGIDs.HydrogenNucleus,
        PDGIDs.Carbon12,
    )
    _non_nuclei = [pid for pid in PDGIDs if pid not in _nuclei]
    for pid in _nuclei:
        assert is_nucleus(pid)
    for pid in _non_nuclei:
        assert not is_nucleus(pid)
    # test 10-digit IDs that does not conform with form for nuclei (should start with +/- 10)
    assert not is_nucleus(2000000010)
    assert not is_nucleus(1100000010)


def test_is_diquark(PDGIDs):
    _diquarks = (PDGIDs.DD1, PDGIDs.SD0)
    _non_diquarks = [pid for pid in PDGIDs if pid not in _diquarks]
    for pid in _diquarks:
        assert is_diquark(pid)
    for pid in _non_diquarks:
        assert not is_diquark(pid)


def test_is_Rhadron(PDGIDs):
    _Rhadrons = (PDGIDs.RPlus_TTildeDbar, PDGIDs.R0_GTildeG, PDGIDs.RPlusPlus_GTildeUUU)
    _non_Rhadrons = [pid for pid in PDGIDs if pid not in _Rhadrons]
    for pid in _Rhadrons:
        assert is_Rhadron(pid)
    for pid in _non_Rhadrons:
        assert not is_Rhadron(pid)


def test_is_Qball(PDGIDs):
    _Qballs = (PDGIDs.QBall1, PDGIDs.QBall2)
    _non_Qballs = [pid for pid in PDGIDs if pid not in _Qballs]
    for pid in _Qballs:
        assert is_Qball(pid)
    for pid in _non_Qballs:
        assert not is_Qball(pid)


def test_is_dyon(PDGIDs):
    _dyons = (PDGIDs.DyonSameMagElecChargeSign, PDGIDs.DyonOppositeMagElecChargeSign)
    _non_dyons = [pid for pid in PDGIDs if pid not in _dyons]
    for pid in _dyons:
        assert is_dyon(pid)
    for pid in _non_dyons:
        assert not is_dyon(pid)


def test_is_SUSY(PDGIDs):
    _susy = (
        PDGIDs.Gluino,
        PDGIDs.Gravitino,
        PDGIDs.STildeL,
        PDGIDs.CTildeR,
        PDGIDs.R0_1000017,
    )
    _non_susy = [pid for pid in PDGIDs if pid not in _susy]
    for pid in _susy:
        assert is_SUSY(pid)
    for pid in _non_susy:
        assert not is_SUSY(pid)


def test_is_technicolor(PDGIDs):
    _technicolor = (PDGIDs.Pi0TC, PDGIDs.PiMinusTC)
    _non_technicolor = [pid for pid in PDGIDs if pid not in _technicolor]
    for pid in _technicolor:
        assert is_technicolor(pid)
    for pid in _non_technicolor:
        assert not is_technicolor(pid)


def test_is_excited_quark_or_lepton(PDGIDs):
    _excited_quark_or_lepton = (PDGIDs.UQuarkStar, PDGIDs.AntiElectronStar)
    _non_excited_quark_or_lepton = [
        pid for pid in PDGIDs if pid not in _excited_quark_or_lepton
    ]
    for pid in _excited_quark_or_lepton:
        assert is_excited_quark_or_lepton(pid)
    for pid in _non_excited_quark_or_lepton:
        assert not is_excited_quark_or_lepton(pid)


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
    assert has_down(PDGIDs.N1650Plus)
    assert has_down(PDGIDs.Lambda1810)
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
    assert has_up(PDGIDs.N1900BarMinus)
    assert has_up(PDGIDs.Lambda1810)
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
    assert not has_strange(PDGIDs.N1650Plus)
    assert has_strange(PDGIDs.Lambda1810)
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
        PDGIDs.psi_3770,
        PDGIDs.D0,
        PDGIDs.DPlus,
        PDGIDs.DsPlus,
        PDGIDs.BcPlus,
        PDGIDs.LcPlus,
        PDGIDs.UCbarCUDPentaquark,
        PDGIDs.AntiUCbarCUDPentaquark,
    )
    _without_charm_content = [pid for pid in PDGIDs if pid not in _with_charm_content]
    for pid in _with_charm_content:
        assert has_charm(pid)
    for pid in _without_charm_content:
        assert not has_charm(pid)


def test_has_bottom(PDGIDs):
    _with_bottom_content = (
        PDGIDs.Upsilon_1S,
        PDGIDs.Upsilon_4S,
        PDGIDs.Upsilon_3_2D,
        PDGIDs.h_b_3P,
        PDGIDs.B0,
        PDGIDs.BPlus,
        PDGIDs.Bs,
        PDGIDs.BcPlus,
        PDGIDs.Lb,
    )
    _without_bottom_content = [pid for pid in PDGIDs if pid not in _with_bottom_content]
    for pid in _with_bottom_content:
        assert has_bottom(pid)
    for pid in _without_bottom_content:
        assert not has_bottom(pid)


def test_has_top(PDGIDs):
    assert has_top(PDGIDs.T0)
    assert has_top(PDGIDs.LtPlus)
    _no_top = [
        pid for pid in PDGIDs if pid not in (PDGIDs.T0, PDGIDs.LtPlus)
    ]  # top quark should also return has_top(6)==False !
    for pid in _no_top:
        assert not has_top(pid)


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
        PDGIDs.R0_1000017,
    )
    _nope = [pid for pid in PDGIDs if pid not in _yep]
    for pid in _yep:
        assert has_fundamental_anti(pid)
    for pid in _nope:
        assert not has_fundamental_anti(pid)


def _mesons_JSL_states_list(PDGIDs, jsl):
    """
    Trivial helper to organise mesons to be tested
    according to their J, S and L quantum numbers.
    """
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
        "101": (PDGIDs.K1_1270_0, PDGIDs.h_b_3P),
        "110": (PDGIDs.rho_770_minus, PDGIDs.jpsi, PDGIDs.Upsilon_4S),
        "111": (PDGIDs.K1_1400_0,),
        "112": (PDGIDs.rho_1700_0, PDGIDs.psi_3770),
        "202": (PDGIDs.K2_1770_minus,),
        "211": (PDGIDs.a2_1320_minus,),
        "212": (PDGIDs.K2_1820_0_bar,),
        "213": (PDGIDs.f_2_30225,),
        "303": (PDGIDs.K3_10317_0,),
        "312": (PDGIDs.omega_3_1670, PDGIDs.Upsilon_3_2D),
        "313": (PDGIDs.K3_20317_plus,),
        "314": (PDGIDs.K3_30317_0,),
        "404": (PDGIDs.rho_10219_plus,),
        "413": (PDGIDs.f_4_2050,),
        "414": (PDGIDs.K4_20219_minus,),
        "415": (PDGIDs.K4_30329_plus,),
    }
    return _states[jsl]


def test_JSL_mesons(PDGIDs):
    _JSL_eq_000 = _mesons_JSL_states_list(PDGIDs, "000")
    _JSL_eq_011 = _mesons_JSL_states_list(PDGIDs, "011")
    _JSL_eq_101 = _mesons_JSL_states_list(PDGIDs, "101")
    _JSL_eq_110 = _mesons_JSL_states_list(PDGIDs, "110")
    _JSL_eq_111 = _mesons_JSL_states_list(PDGIDs, "111")
    _JSL_eq_112 = _mesons_JSL_states_list(PDGIDs, "112")
    _JSL_eq_202 = _mesons_JSL_states_list(PDGIDs, "202")
    _JSL_eq_211 = _mesons_JSL_states_list(PDGIDs, "211")
    _JSL_eq_212 = _mesons_JSL_states_list(PDGIDs, "212")
    _JSL_eq_213 = _mesons_JSL_states_list(PDGIDs, "213")
    _JSL_eq_303 = _mesons_JSL_states_list(PDGIDs, "303")
    _JSL_eq_312 = _mesons_JSL_states_list(PDGIDs, "312")
    _JSL_eq_313 = _mesons_JSL_states_list(PDGIDs, "313")
    _JSL_eq_314 = _mesons_JSL_states_list(PDGIDs, "314")
    _JSL_eq_404 = _mesons_JSL_states_list(PDGIDs, "404")
    _JSL_eq_413 = _mesons_JSL_states_list(PDGIDs, "413")
    _JSL_eq_414 = _mesons_JSL_states_list(PDGIDs, "414")
    _JSL_eq_415 = _mesons_JSL_states_list(PDGIDs, "415")

    for pid in _JSL_eq_000:
        assert J(pid) == 0
        assert S(pid) == 0
        assert L(pid) == 0
    for pid in _JSL_eq_011:
        assert J(pid) == 0
        assert S(pid) == 1
        assert L(pid) == 1
    for pid in _JSL_eq_101:
        assert J(pid) == 1
        assert S(pid) == 0
        assert L(pid) == 1
    for pid in _JSL_eq_110:
        assert J(pid) == 1
        assert S(pid) == 1
        assert L(pid) == 0
    for pid in _JSL_eq_111:
        assert J(pid) == 1
        assert S(pid) == 1
        assert L(pid) == 1
    for pid in _JSL_eq_112:
        assert J(pid) == 1
        assert S(pid) == 1
        assert L(pid) == 2
    for pid in _JSL_eq_202:
        assert J(pid) == 2
        assert S(pid) == 0
        assert L(pid) == 2
    for pid in _JSL_eq_211:
        assert J(pid) == 2
        assert S(pid) == 1
        assert L(pid) == 1
    for pid in _JSL_eq_212:
        assert J(pid) == 2
        assert S(pid) == 1
        assert L(pid) == 2
    for pid in _JSL_eq_213:
        assert J(pid) == 2
        assert S(pid) == 1
        assert L(pid) == 3
    for pid in _JSL_eq_303:
        assert J(pid) == 3
        assert S(pid) == 0
        assert L(pid) == 3
    for pid in _JSL_eq_312:
        assert J(pid) == 3
        assert S(pid) == 1
        assert L(pid) == 2
    for pid in _JSL_eq_313:
        assert J(pid) == 3
        assert S(pid) == 1
        assert L(pid) == 3
    for pid in _JSL_eq_314:
        assert J(pid) == 3
        assert S(pid) == 1
        assert L(pid) == 4
    for pid in _JSL_eq_404:
        assert J(pid) == 4
        assert S(pid) == 0
        assert L(pid) == 4
    for pid in _JSL_eq_413:
        assert J(pid) == 4
        assert S(pid) == 1
        assert L(pid) == 3
    for pid in _JSL_eq_414:
        assert J(pid) == 4
        assert S(pid) == 1
        assert L(pid) == 4
    for pid in _JSL_eq_415:
        assert J(pid) == 4
        assert S(pid) == 1
        assert L(pid) == 5


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

    for pid in _J_eq_0:
        assert j_spin(pid) == 1
    for pid in _J_eq_1:
        assert j_spin(pid) == 3
    for pid in _J_eq_1over2:
        assert j_spin(pid) == 2
    for pid in _J_eq_3over2:
        assert j_spin(pid) == 4
    for pid in _invalid_pdgids:
        assert j_spin(pid) is None
    for pid in _J_eq_None:
        assert j_spin(pid) is None
    # Alternative ID=9 for the gluon in codes for glueballs to allow a notation in close analogy with that of hadrons
    assert j_spin(9) == 3


def test_S_non_mesons(PDGIDs):
    for pid in _get_non_mesons(PDGIDs):
        assert S(pid) is None


def test_L_non_mesons(PDGIDs):
    for pid in _get_non_mesons(PDGIDs):
        assert L(pid) is None


def test_A(PDGIDs):
    _nuclei = {
        PDGIDs.Proton: 1,
        PDGIDs.AntiNeutron: 1,
        PDGIDs.HydrogenNucleus: 1,
        PDGIDs.Carbon12: 12,
    }
    _non_nuclei = [pid for pid in PDGIDs if pid not in _nuclei.keys()]
    for pid, a in _nuclei.items():
        assert A(pid) == a
    for pid in _non_nuclei:
        assert A(pid) is None


def test_Z(PDGIDs):
    _nuclei = {
        PDGIDs.Proton: 1,
        PDGIDs.AntiNeutron: 0,
        PDGIDs.HydrogenNucleus: 1,
        PDGIDs.Carbon12: 6,
    }
    _non_nuclei = [pid for pid in PDGIDs if pid not in _nuclei.keys()]
    for pid, z in _nuclei.items():
        assert Z(pid) == z
    for pid in _non_nuclei:
        assert Z(pid) is None
