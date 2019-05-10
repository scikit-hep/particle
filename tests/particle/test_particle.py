# -*- encoding: utf-8 -*-
# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import, division, print_function

import sys


try:
    from pathlib2 import Path
except ImportError:
    from pathlib import Path

import pytest
from pytest import approx

from particle.particle.enums import Charge, SpinType
from particle.particle import Particle
from particle.particle.particle import ParticleNotFound, InvalidParticle
from particle.pdgid import PDGID

from hepunits.units import second


DIR = Path(__file__).parent.resolve()


def test_find():
    # 1 match found
    prepr = repr(Particle.find(name='gamma'))
    assert prepr == '<Particle: name="gamma", pdgid=22, mass=0.0 MeV>'

    # No match found
    with pytest.raises(ParticleNotFound):
        Particle.find(name='NonExistent')

    # Multiple matches found
    with pytest.raises(RuntimeError):
        Particle.find(name=lambda x: 'Upsilon' in x)


def test_lambda_style_search():
    particles = Particle.findall(lambda p: p.pdg_name == 'p')
    assert len(particles) == 2
    assert 2212 in particles
    assert -2212 in particles

    assert Particle.find(lambda p: p.pdg_name == 'p' and p > 0) == 2212
    assert Particle.find(lambda p: p.pdg_name == 'p' and p < 0) == -2212


def test_fuzzy_name_search():
    particles = Particle.findall('p~')
    assert len(particles) == 1
    assert -2212 in particles


def test_keyword_style_search():
    particles = Particle.findall(pdg_name = 'p')
    assert len(particles) == 2
    assert 2212 in particles
    assert -2212 in particles

    particles = Particle.findall(name = 'p')
    assert len(particles) == 1
    assert 2212 in particles

    assert Particle.find(pdg_name = 'p', particle=True) == 2212
    assert Particle.find(pdg_name = 'p', particle=False) == -2212

    assert Particle.find(name = 'p', particle=True) == 2212
    assert Particle.find(name = 'p~', particle=False) == -2212


def test_keyword_lambda_style_search():
    particles = Particle.findall(pdg_name = lambda x: 'p' == x)
    assert len(particles) == 2
    assert 2212 in particles
    assert -2212 in particles

    # Fuzzy name
    particles = Particle.findall(name = lambda x: 'p' in x)
    assert len(particles) > 2
    assert 2212 in particles
    assert -2212 in particles

    # Name and particle
    assert Particle.find(name = lambda x: x == 'p', particle=True) == 2212

    # Unit based comparison
    assert 2212 in Particle.findall(lifetime = lambda x : x > 1*second)


def test_complex_search():
    # Find all strange mesons with c*tau > 1 meter
    particles = Particle.findall(lambda p: p.pdgid.is_meson and p.pdgid.has_strange and p.width > 0 and p.ctau > 1000., particle=True)
    assert len(particles) == 2 # K+ and KL0
    assert 130 in particles
    assert 321 in particles

    # Find all strange anti-mesons with c*tau > 1 meter
    particles = Particle.findall(lambda p: p.pdgid.is_meson and p.pdgid.has_strange and p.width > 0 and p.ctau > 1000., particle=False)
    assert len(particles) == 1 # only the K-
    assert -321 in particles


def test_pdg():
    assert Particle.from_pdgid(211).pdgid == 211
    with pytest.raises(InvalidParticle):
        Particle.from_pdgid(0)


def test_pdg_convert():
    p = Particle.from_pdgid(211)
    assert isinstance(p.pdgid, PDGID)
    assert int(p) == 211
    assert PDGID(p) == 211


def test_sorting():
    assert Particle.from_pdgid(211) < Particle.from_pdgid(311)
    assert Particle.from_pdgid(211) < Particle.from_pdgid(-311)


def test_int_compare():
    assert Particle.from_pdgid(211) > 0
    assert Particle.from_pdgid(-211) < 0
    assert Particle.from_pdgid(211) >= 0
    assert Particle.from_pdgid(-211) <= 0

    assert 0 < Particle.from_pdgid(211)
    assert 0 > Particle.from_pdgid(-211)
    assert 0 <= Particle.from_pdgid(211)
    assert 0 >= Particle.from_pdgid(-211)


def test_str():
    pi = Particle.from_pdgid(211)
    assert str(pi) == 'pi+'


def test_rep():
    pi = Particle.from_pdgid(211)
    assert "pdgid=211" in repr(pi)
    assert 'name="pi+"' in repr(pi)
    assert "mass=139.57" in repr(pi)


def test_basic_props():
    pi = Particle.from_pdgid(211)
    assert pi.pdg_name == 'pi'
    assert pi.pdgid == 211
    assert pi.three_charge == Charge.p
    assert pi.charge == 1


def test_lifetime_props():
    pi = Particle.from_pdgid(211)
    assert pi.lifetime == approx(26.0327460625985)   # in nanoseconds
    assert pi.ctau == approx(7804.4209306)   # in millimeters


def test_charge_consistency():
    """
    The charge of a particle is presently stored in the CSV files
    (see Particle.charge for the motivation), but it can also be retrieved
    from the particle's PDG ID, *if* the latter is valid.
    This test makes sure both numbers are consistent for all particles in the PDG table.
    """
    for p in Particle.table():
        assert p.three_charge == p.pdgid.three_charge


def test_describe():
    # Test print-out of symmetric lifetime errors
    __description = u'Lifetime = 26.033 ± 0.005 ns'
    if sys.version_info < (3, 0):
        __description = __description.replace(u'±', u'+/-')
    pi = Particle.from_pdgid(211)
    assert __description in pi.describe()

    # Test print-out of asymmetric lifetime errors
    __description = 'Lifetime = 1.12e+09 + 1.7e+08 - 1.6e+08 ns'
    Omega_b_minus = Particle.from_pdgid(5332)
    assert __description in Omega_b_minus.describe()

    # Test print-out of symmetric width errors
    __description = u'Width = 2495.2 ± 2.3 MeV'
    if sys.version_info < (3, 0):
        __description = __description.replace(u'±', u'+/-')
    H0 = Particle.from_pdgid(23)
    assert __description in H0.describe()

    # Test print-out of asymmetric width errors
    __description = 'Width = 1.89 + 0.09 - 0.18 MeV'
    Sigma_c_pp = Particle.from_pdgid(4222)
    assert __description in Sigma_c_pp.describe()

    # Test print-out of zero width values
    __description = r"""Name: gamma          ID: 22           Latex: $\gamma$
Mass  = 0.0 MeV
Width = 0.0 MeV
Q (charge)        = 0       J (total angular) = 1.0      P (space parity) = -
C (charge parity) = -       I (isospin)       = <2       G (G-parity)     = ?
    SpinType: SpinType.Vector
    Antiparticle name: gamma (antiparticle status: Same)"""
    photon = Particle.from_pdgid(22)
    assert photon.describe() == __description


def test_default_table_loading():
    Particle.table()
    p = Particle.from_pdgid(211)
    assert p.table_loaded() is True
    assert p.table_names() == ('particle2018.csv',)


def test_default_table_loading_bis():
    assert Particle.table_names() == ('particle2018.csv',)


def test_explicit_table_loading():
    Particle.load_table(DIR / '../../particle/data/particle2018.csv')
    assert Particle.table_loaded() == True
    assert len(Particle.table_names()) == 1
    assert Particle.table() is not None


checklist_html_name = (
    (22, 'γ'),                           # photon
    (1, 'd'),                            # d quark
    (-2, '<SPAN STYLE="text-decoration:overline">u</SPAN>'),  # u antiquark
    (11, 'e<SUP>-</SUP>'),               # e-
    (-13, 'μ<SUP>+</SUP>'),              # mu+
    (-14, '<SPAN STYLE="text-decoration:overline">ν</SPAN><SUB>μ</SUB>'),  # nu_mu_bar
    (111, 'π<SUP>0</SUP>'),              # pi0
    (-211, 'π<SUP>-</SUP>'),             # pi-
    (-213, 'ρ(770)<SUP>-</SUP>'),        # rho(770)-
    (20213, 'a<SUB>1</SUB>(1260)<SUP>+</SUP>'),# a_1(1260)+
    (321, 'K<SUP>+</SUP>'),              # K+
    (130, 'K<SUB>L</SUB><SUP>0</SUP>'),  # K_L
    (10321, 'K<SUB>0</SUB><SUP>*</SUP>(1430)<SUP>+</SUP>'), # K(0)*(1430)+
    (-10321, 'K<SUB>0</SUB><SUP>*</SUP>(1430)<SUP>-</SUP>'),  # K(0)*(1430)-
    (10433, 'D<SUB>s1</SUB>(2536)/D<SUB>s1</SUB><SUP>+</SUP>(L)<SUP>+</SUP>'),           # D_s1(2536)+
    (-511, '<SPAN STYLE="text-decoration:overline">B</SPAN><SUP>0</SUP>'),               # B0_bar
    (443, 'J/ψ(1S)'),                    # J/psi
    (10441, 'χ<SUB>c0</SUB>(1P)'),       # chi_c0(1P)
    (300553, 'Υ(4S)'),                   # Upsilon(4S)
    (2212, 'p'),                         # proton
    (-2112, '<SPAN STYLE="text-decoration:overline">n</SPAN>'),                          # antineutron
    (-2224, '<SPAN STYLE="text-decoration:overline">Δ</SPAN>(1232)<SUP>--</SUP>'),       # Delta_bar(1232)--
    (3322, 'Ξ<SUP>0</SUP>'),             # Xi0
    (-3322, '<SPAN STYLE="text-decoration:overline">Ξ</SPAN><SUP>0</SUP>'),              # Xi0_bar
    (-5122, '<SPAN STYLE="text-decoration:overline">Λ</SPAN><SUB>b</SUB><SUP>0</SUP>')   # Lb0_bar
)


@pytest.mark.skipif(sys.version_info < (3,0), reason="Requires Python 3")
@pytest.mark.parametrize("pid,html_name", checklist_html_name)
def test_html_name(pid, html_name):
    particle = Particle.from_pdgid(pid)

    assert particle.html_name == html_name


checklist_is_self_conjugate = (
    (1, False),       # d quark
    (-13, False),     # mu+
    (111, True),      # pi0
    (211, False),     # pi+
    (-211, False),    # pi-
    (443, True),      # J/psi
    (300553, True),   # Upsilon(4S)
    (130, True),      # K_L
    (2212, False),    # proton
    (-2112, False),   # antineutron
    (3322, False),    # Xi0
    (-3322, False),   # Xi0_bar
    (-511, False),    # B0_bar
    (5122, False),    # Lb0
)


@pytest.mark.parametrize("pid,is_self_conjugate", checklist_is_self_conjugate)
def test_is_self_conjugate(pid, is_self_conjugate):
    particle = Particle.from_pdgid(pid)

    assert particle.is_self_conjugate == is_self_conjugate


checklist_is_name_barred = (
    (1, False),       # d quark
    (-2, True),       # u antiquark
    (11, False),      # e-
    (-13, False),     # mu+
    (111, False),     # pi0
    (211, False),     # pi+
    (-211, False),    # pi-
    (-213, False),    # rho(770)-
    (443, False),     # J/psi
    (300553, False),  # Upsilon(4S)
    (130, False),     # K_L
    (2212, False),    # proton
    (-2112, True),    # antineutron
    (3322, False),    # Xi0
    (-3322, True),    # Xi0_bar
    (-511, True),     # B0_bar
    (-5122, True),    # Lb0_bar
)


@pytest.mark.parametrize("pid,has_bar", checklist_is_name_barred)
def test_is_name_barred(pid, has_bar):
    particle = Particle.from_pdgid(pid)

    assert particle.is_name_barred == has_bar


spin_type_classification = (
    # Gauge bosons
    (23, SpinType.Unknown),      # Z0 - no parity defined for it
    # Leptons aren't assigned a SpinType
    (11, SpinType.NonDefined),      # e-
    # Only mesons are given a SpinType
    # - Pseudo-scalars J^P = 0^-
    (211, SpinType.PseudoScalar),   # pi+
    (310, SpinType.PseudoScalar),   # K_S
    (-421, SpinType.PseudoScalar),  # D0_bar
    # - Scalars J^P = 0^+
    (9000211, SpinType.Scalar),     # a_0(980)+
    (9010221, SpinType.Scalar),     # f_0(980)
    # - Vector J^P = 1^-
    (333, SpinType.Vector),         # phi(1020)
    (443, SpinType.Vector),         # J/psi
    # Axial-vector - J^P = 1^+
    (20213, SpinType.Axial),        # a_1(1260)+
    (20313, SpinType.Axial),        # K_1(1400)0
    (10433, SpinType.Axial),        # D_s1(2536)+
    # Tensor - J^P = 2^+
    (225, SpinType.Tensor),         # f_2(1270)
    (315, SpinType.Tensor),         # K*_2(1430)0
    # Pseudo-tensor - J^P = 2^-
    (10225, SpinType.PseudoTensor), # eta_2(1645)
    # J > 2 mesons
    (329, SpinType.Unknown),        # K*_4(2045)+
    # Baryons aren't assigned a SpinType
    (2212, SpinType.NonDefined),    # proton
)


@pytest.mark.parametrize("pid,stype", spin_type_classification)
def test_spin_type(pid, stype):
    particle = Particle.from_pdgid(pid)

    assert particle.spin_type == stype


ampgen_style_names = (
    ("b", 5),
    ("b~", -5),
    ("pi+", 211),
    ("pi-", -211),
    ("K~*0", -313),
    ("K*(892)bar0", -313),
    ("a(1)(1260)+", 20213),
    ("rho(1450)0", 100113),
    ("rho(770)0", 113),
    ("K(1)(1270)bar-", -10323),
    ("K(1460)bar-", -100321),
    ("K(2)*(1430)bar-", -325)
)


@pytest.mark.parametrize("name,pid", ampgen_style_names)
def test_ampgen_style_names(name, pid):
    particle = Particle.from_string(name)

    assert int(particle) == pid
    assert particle.pdgid == pid
    assert particle == pid


decfile_style_names = (
    ("s", 3),
    ("anti-b", -5),
    ("anti-K*0", -313),
    ("eta", 221),
    ("eta'", 331),
    ("a_0+", 9000211),
    ("a_00", 9000111),
    ("a_1-", -20213),
    ("a_10", 20113),
    ("f_0", 9010221),
    ("f'_0", 10221),
    ("f_1", 20223),
    ("f'_1", 20333),
    ("f'_2", 335),
    ("h_1", 10223),
    ("h'_1", 10333),
    ("rho+", 213),
    ("rho(2S)0", 100113),
    ("omega", 223),
    ("omega(2S)", 1000223),
    ("omega(1650)", 30223),
    ("Delta++", 2224),
    ("Delta+", 2214),
    ("Delta0", 2114),
    ("Delta-", 1114),
    ("D+", 411),
    ("D'_1+", 10413),
    ("anti-D'_10", -10423),
    ("D_2*+", 415),
    ("D_s+", 431),
    ("anti-B0", -511),
    ("B+", 521),
    ("B-", -521),
    ("B*+", 523),
    ("B*-", -523),
    ("N(1440)+", 12212),
    ("anti-N(1440)-", -12212),
    ("anti-Lambda_b0", -5122),
    ("Sigma_b+", 5222),
    ("Sigma_b0", 5212),
    ("Sigma_b-", 5112),
    ("anti-Sigma_b-", -5222),
    ("anti-Sigma_b0", -5212),
    ("anti-Sigma_b+", -5112),
    ("Sigma_b*+", 5224),
    ("Sigma_b*0", 5214),
    ("Sigma_b*-", 5114),
    ("anti-Sigma_b*-", -5224),
    ("anti-Sigma_b*0", -5214),
    ("anti-Sigma_b*+", -5114)
)


@pytest.mark.parametrize("name,pid", decfile_style_names)
def test_decfile_style_names(name, pid):
    assert Particle.from_dec(name).pdgid == pid
