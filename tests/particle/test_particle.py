# -*- encoding: utf-8 -*-
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import, division, print_function

import sys

import pytest
from pytest import approx

from particle.particle.enums import Charge, Parity, SpinType, Status, Inv
from particle.particle import Particle
from particle.particle.particle import ParticleNotFound, InvalidParticle
from particle.pdgid import PDGID
from particle.pdgid.functions import _digit, Location
from particle import data

from hepunits import second, meter


def test_find():
    # 1 match found
    prepr = repr(Particle.find(name="gamma"))
    assert prepr == '<Particle: name="gamma", pdgid=22, mass=0.0 MeV>'

    # No match found
    with pytest.raises(ParticleNotFound):
        Particle.find(name="NotInPDT")

    # Multiple matches found
    with pytest.raises(RuntimeError):
        Particle.find(name=lambda x: "Upsilon" in x)


def test_lambda_style_search():
    particles = Particle.findall(lambda p: p.pdg_name == "p")
    assert len(particles) == 4
    assert 2212 in particles
    assert -2212 in particles
    assert 1000010010 in particles
    assert -1000010010 in particles

    [p.pdgid for p in Particle.findall(lambda p: p.pdg_name == "p" and p > 0)] == [
        2212,
        1000010010,
    ]
    [p.pdgid for p in Particle.findall(lambda p: p.pdg_name == "p" and p < 0)] == [
        -2212,
        -1000010010,
    ]


def test_fuzzy_name_search():
    particles = Particle.findall("p~")
    assert len(particles) == 2
    assert -2212 in particles
    assert -1000010010 in particles


def test_keyword_style_search():
    particles = Particle.findall(pdg_name="p")
    assert len(particles) == 4
    assert 2212 in particles
    assert -2212 in particles
    assert 1000010010 in particles
    assert -1000010010 in particles


def test_keyword_style_search_with_except_catch():
    particles = Particle.findall(ctau=float("inf"))
    assert 11 in particles

    particles = Particle.findall(name="p")
    assert len(particles) == 2
    assert 2212 in particles
    assert 1000010010 in particles

    [p.pdgid for p in Particle.findall(pdg_name="p", particle=True)] == [
        2212,
        1000010010,
    ]
    [p.pdgid for p in Particle.findall(pdg_name="p", particle=False)] == [
        -2212,
        -1000010010,
    ]

    [p.pdgid for p in Particle.findall(name="p", particle=True)] == [2212, 1000010010]
    [p.pdgid for p in Particle.findall(name="p~", particle=False)] == [
        -2212,
        -1000010010,
    ]


def test_keyword_lambda_style_search():
    particles = Particle.findall(pdg_name=lambda x: "p" == x)
    assert len(particles) == 4
    assert 2212 in particles
    assert -2212 in particles
    assert 1000010010 in particles
    assert -1000010010 in particles

    # Fuzzy name
    particles = Particle.findall(name=lambda x: "p" in x)
    assert len(particles) > 2
    assert 2212 in particles
    assert -2212 in particles

    # Name and particle
    assert len(Particle.findall(name=lambda x: x == "p", particle=True)) == 2

    # Unit based comparison
    assert 2212 in Particle.findall(lifetime=lambda x: x > 1 * second)


def test_complex_search():
    # Find all strange mesons with c*tau > 1 meter
    particles = Particle.findall(
        lambda p: p.pdgid.is_meson
        and p.pdgid.has_strange
        and p.width > 0
        and p.ctau > 1000.0,
        particle=True,
    )
    assert len(particles) == 2  # K+ and KL0
    assert 130 in particles
    assert 321 in particles

    # Find all strange anti-mesons with c*tau > 1 meter
    particles = Particle.findall(
        lambda p: p.pdgid.is_meson
        and p.pdgid.has_strange
        and p.width > 0
        and p.ctau > 1000.0,
        particle=False,
    )
    assert len(particles) == 1  # only the K-
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


def test_string():
    pi = Particle.from_string("pi+")
    assert pi.pdgid == 211

    with pytest.raises(ParticleNotFound):
        Particle.from_string("unknown")


def test_fuzzy_string():
    """
    The input name is not specific enough, in which case the search is done
    by pdg_name after failing a match by name.
    """
    p = Particle.from_string("a(0)(980)")  # all 3 charge stages match
    assert p.pdgid == 9000111


def test_str():
    pi = Particle.from_pdgid(211)
    assert str(pi) == "pi+"


def test_rep():
    pi = Particle.from_pdgid(211)
    assert "pdgid=211" in repr(pi)
    assert 'name="pi+"' in repr(pi)
    assert "mass=139.57" in repr(pi)


def test_basic_props():
    pi = Particle.from_pdgid(211)
    assert pi.pdg_name == "pi"
    assert pi.pdgid == 211
    assert pi.three_charge == Charge.p
    assert pi.charge == 1


def test_lifetime_props():
    pi = Particle.from_pdgid(211)
    assert pi.lifetime == approx(26.0327460625985)  # in nanoseconds
    assert pi.ctau == approx(7804.4209306)  # in millimeters


def test_charge_consistency():
    """
    The charge of a particle is presently stored in the CSV files
    (see Particle.charge for the motivation), but it can also be retrieved
    from the particle's PDG ID, *if* the latter is valid.
    This test makes sure both numbers are consistent for all particles in the PDG table.
    """
    for p in Particle.all():
        assert p.three_charge == p.pdgid.three_charge


def test_P_consistency():
    """
    The parity quantum number is stored in the (curated) data CSV files.
    For unflavoured mesons it can be calculated as P = (-1)^(L+1),
    and this relation can be checked against the CSV data.

    Note: mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally
    well-known particles and P is undefined.
    """
    for p in Particle.all():
        if not p.is_unflavoured_meson:
            continue
        elif _digit(p.pdgid, Location.N) == 9:
            continue
        elif p.pdgid == 22:  # Special case of the photon
            assert p.P == -1
        else:
            assert p.P == (-1) ** (p.L + 1)


def test_C_consistency():
    """
    The charge conjugation parity is stored in the (curated) data CSV files.
    For unflavoured mesons it can be calculated as C = (-1)^(L+S),
    and this relation can be checked against the CSV data.

    Note: mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally
    well-known particles and C is undefined.
    """
    for p in Particle.all():
        if not p.is_unflavoured_meson:
            continue
        elif _digit(p.pdgid, Location.N) == 9:
            continue
        elif p.pdgid == 22:  # Special case of the photon
            assert p.C == -1
        elif p.pdgid in [130, 310]:  # Special case of the KS and KL
            assert p.C == Parity.u
        else:
            assert p.C == (-1) ** (p.L + p.S)


checklist_describe = (
    # Test undefined width value
    [1, "Width = None"],  # d quark
    # Test print-out of zero width values
    [22, "Width = 0.0 MeV"],  # photon
    # Test print-out of symmetric width errors
    [413, u"Width = 0.0834 ± 0.0018 MeV"],  # D*(2010)+
    [443, u"Width = 0.093 ± 0.003 MeV"],  # J/psi
    # Test print-out of asymmetric width errors
    [4222, "Width = 1.89 + 0.09 - 0.18 MeV"],  # Sigma_c(2455)++
    [23, u"Width = 2495.2 ± 2.3 MeV"],  # H0
    # Test print-out of symmetric lifetime errors
    [5332, u"Lifetime = 1.65e-03 ± 1.8e-04 ns"],  # Omega_b-
    [211, u"Lifetime = 26.033 ± 0.005 ns"],  # pion
    # Test print-out of asymmetric lifetime errors
    [4332, "Lifetime = 2.7e-04 + 3e-05 - 3e-05 ns"],  # Omega_c^0
    # Test particles with at present an upper limit on their width
    [423, "Width < 2.1 MeV"],  # D*(2007)0
    [10431, "Width < 10.0 MeV"],  # D(s0)*(2317)+
    [20433, "Width < 6.3 MeV"],  # D(s1)(2460)+
    [4212, "Width < 4.6 MeV"],  # Sigma(c)(2455)+
    [4214, "Width < 17.0 MeV"],  # Sigma(c)(2520)+
)
if sys.version_info < (3, 0):
    for i, pair_vals in enumerate(checklist_describe):
        checklist_describe[i][1] = pair_vals[1].replace(u"±", u"+/-")


@pytest.mark.parametrize("pid,description", checklist_describe)
def test_describe(pid, description):
    particle = Particle.from_pdgid(pid)
    assert description in particle.describe()


def test_default_table_loading():
    assert Particle.table_names() == ("particle2019.csv", "nuclei2020.csv")


def test_default_table_loading_bis():
    Particle.all()
    p = Particle.from_pdgid(211)
    assert p.table_loaded() is True
    assert p.table_names() == ("particle2019.csv", "nuclei2020.csv")


def test_explicit_table_loading():
    Particle.load_table(data.open_text(data, "particle2019.csv"))
    assert Particle.table_loaded() == True
    assert len(Particle.table_names()) == 1
    assert Particle.all() is not None


checklist_html_name = (
    (22, "&gamma;"),  # photon
    (1, "d"),  # d quark
    (-2, "u&#773;"),  # u antiquark
    (11, "e<SUP>-</SUP>"),  # e-
    (-13, "&mu;<SUP>+</SUP>"),  # mu+
    (-14, "&nu;&#773;<SUB>&mu;</SUB>"),  # nu_mu_bar
    (111, "&pi;<SUP>0</SUP>"),  # pi0
    (-211, "&pi;<SUP>-</SUP>"),  # pi-
    (-213, "&rho;(770)<SUP>-</SUP>"),  # rho(770)-
    (20213, "a<SUB>1</SUB>(1260)<SUP>+</SUP>"),  # a_1(1260)+
    (321, "K<SUP>+</SUP>"),  # K+
    (130, "K<SUB>L</SUB><SUP>0</SUP>"),  # K_L
    (10321, "K<SUB>0</SUB><SUP>*</SUP>(1430)<SUP>+</SUP>"),  # K(0)*(1430)+
    (-10321, "K<SUB>0</SUB><SUP>*</SUP>(1430)<SUP>-</SUP>"),  # K(0)*(1430)-
    (10433, "D<SUB>s1</SUB>(2536)<SUP>+</SUP>"),  # D_s1(2536)+
    (-511, "B&#773;<SUP>0</SUP>"),  # B0_bar
    (443, "J/&psi;(1S)"),  # J/psi
    (10441, "&chi;<SUB>c0</SUB>(1P)"),  # chi_c0(1P)
    (300553, "&Upsilon;(4S)"),  # Upsilon(4S)
    (2212, "p"),  # proton
    (-2112, "n&#773;"),  # antineutron
    (-2224, "&Delta;&#773;(1232)<SUP>--</SUP>"),  # Delta_bar(1232)--
    (3322, "&Xi;<SUP>0</SUP>"),  # Xi0
    (-3322, "&Xi;&#773;<SUP>0</SUP>"),  # Xi0_bar
    (-5122, "&Lambda;&#773;<SUB>b</SUB><SUP>0</SUP>"),  # Lb0_bar
)


@pytest.mark.skipif(sys.version_info < (3, 0), reason="Requires Python 3")
@pytest.mark.parametrize("pid,html_name", checklist_html_name)
def test_html_name(pid, html_name):
    particle = Particle.from_pdgid(pid)

    assert particle.html_name == html_name


checklist_is_self_conjugate = (
    (1, False),  # d quark
    (-13, False),  # mu+
    (111, True),  # pi0
    (211, False),  # pi+
    (-211, False),  # pi-
    (443, True),  # J/psi
    (300553, True),  # Upsilon(4S)
    (130, True),  # K_L
    (2212, False),  # proton
    (-2112, False),  # antineutron
    (3322, False),  # Xi0
    (-3322, False),  # Xi0_bar
    (-511, False),  # B0_bar
    (5122, False),  # Lb0
)


@pytest.mark.parametrize("pid,is_self_conjugate", checklist_is_self_conjugate)
def test_is_self_conjugate(pid, is_self_conjugate):
    particle = Particle.from_pdgid(pid)

    assert particle.is_self_conjugate == is_self_conjugate


def test_self_conjugation_consistenty():
    """
    The logic implemented in ``Particle.invert()`` and ``Particle.is_self_conjugate``
    should be consistent. In other words, the inverse of
    ``self.anti_flag == Inv.ChargeInv and self.three_charge != Charge.o``
    in ``Particle.invert()`` should match ``Particle.is_self_conjugate``.
    """
    n_inconsistencies = 0

    for p in Particle.all():
        if (
            p.anti_flag == Inv.ChargeInv and p.three_charge == Charge.o
        ) and not p.is_self_conjugate:
            n_inconsistencies += 1

    assert n_inconsistencies == 0


checklist_is_name_barred = (
    (1, False),  # d quark
    (-2, True),  # u antiquark
    (11, False),  # e-
    (-13, False),  # mu+
    (111, False),  # pi0
    (211, False),  # pi+
    (-211, False),  # pi-
    (-213, False),  # rho(770)-
    (443, False),  # J/psi
    (300553, False),  # Upsilon(4S)
    (130, False),  # K_L
    (2212, False),  # proton
    (-2112, True),  # antineutron
    (3322, False),  # Xi0
    (-3322, True),  # Xi0_bar
    (-511, True),  # B0_bar
    (-5122, True),  # Lb0_bar
)


@pytest.mark.parametrize("pid,has_bar", checklist_is_name_barred)
def test_is_name_barred(pid, has_bar):
    particle = Particle.from_pdgid(pid)

    assert particle.is_name_barred == has_bar


spin_type_classification = (
    # Gauge bosons
    (23, SpinType.Unknown),  # Z0 - no parity defined for it
    # Leptons aren't assigned a SpinType
    (11, SpinType.NonDefined),  # e-
    # Only mesons are given a SpinType
    # - Pseudo-scalars J^P = 0^-
    (211, SpinType.PseudoScalar),  # pi+
    (310, SpinType.PseudoScalar),  # K_S
    (-421, SpinType.PseudoScalar),  # D0_bar
    # - Scalars J^P = 0^+
    (9000211, SpinType.Scalar),  # a_0(980)+
    (9010221, SpinType.Scalar),  # f_0(980)
    # - Vector J^P = 1^-
    (333, SpinType.Vector),  # phi(1020)
    (443, SpinType.Vector),  # J/psi
    # Axial-vector - J^P = 1^+
    (20213, SpinType.Axial),  # a_1(1260)+
    (20313, SpinType.Axial),  # K_1(1400)0
    (10433, SpinType.Axial),  # D_s1(2536)+
    # Tensor - J^P = 2^+
    (225, SpinType.Tensor),  # f_2(1270)
    (315, SpinType.Tensor),  # K*_2(1430)0
    # Pseudo-tensor - J^P = 2^-
    (10225, SpinType.PseudoTensor),  # eta_2(1645)
    # J > 2 mesons
    (329, SpinType.Unknown),  # K*_4(2045)+
    # Baryons aren't assigned a SpinType
    (2212, SpinType.NonDefined),  # proton
)


@pytest.mark.parametrize("pid,stype", spin_type_classification)
def test_spin_type(pid, stype):
    particle = Particle.from_pdgid(pid)

    assert particle.spin_type == stype


checklist_isospin = (
    # Quarks
    (1, 0.5),  # d
    # Gauge bosons
    (22, None),  # photon
    (23, None),  # Z0
    # Leptons
    (11, None),  # e-
    (-12, None),  # nu(e)_bar
    # Mesons
    (211, 1.0),  # pi+
    (310, 0.5),  # K_S
    (-421, 0.5),  # D0_bar
    (333, 0.0),  # phi(1020)
    (443, 0.0),  # J/psi
    (521, 0.5),  # B+
    (531, 0.0),  # Bs
    # Baryons
    (2212, 0.5),  # proton
    (2214, 1.5),  # Delta+
)


@pytest.mark.parametrize("pid,isospin", checklist_isospin)
def test_isospin(pid, isospin):
    particle = Particle.from_pdgid(pid)

    assert particle.I == isospin


def test_default_particle():
    p = Particle.empty()

    assert repr(p) == '<Particle: name="Unknown", pdgid=0, mass=None>'
    assert "Name: Unknown" in p.describe()
    assert p.mass == None
    assert p.width == None
    assert p.spin_type == SpinType.NonDefined
    assert p.programmatic_name == "Unknown"
    assert p.status == Status.NotInPDT


def test_dump_table():
    tbl = Particle.dump_table(
        filter_fn=lambda p: p.pdgid.is_meson
        and p.pdgid.has_strange
        and p.ctau > 1 * meter,
        exclusive_fields=["pdgid", "name"],
    )
    assert (
        tbl
        == "  pdgid  name\n-------  ------\n    130  K(L)0\n    321  K+\n   -321  K-"
    )

    tbl = Particle.dump_table(
        filter_fn=lambda p: p.pdgid > 0
        and p.pdgid.is_meson
        and p.pdgid.has_strange
        and p.pdgid.has_charm,
        exclusive_fields=["name"],
        n_rows=2,
        tablefmt="html",
    )

    assert "<td>D(s)+ </td></tr>\n<tr><td>D(s)*+</td>" in tbl


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
    # ("K(1460)bar-", -100321),
    ("K(2)*(1430)bar-", -325),
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
    ("omega(1650)", 30223),
    ("Delta++", 2224),
    ("Delta+", 2214),
    ("Delta0", 2114),
    ("Delta-", 1114),
    ("D+", 411),
    # ("D'_1+", 10413),
    # ("anti-D'_10", -10423),
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
    # ("Sigma_b0", 5212),
    ("Sigma_b-", 5112),
    ("anti-Sigma_b-", -5222),
    # ("anti-Sigma_b0", -5212),
    ("anti-Sigma_b+", -5112),
    ("Sigma_b*+", 5224),
    # ("Sigma_b*0", 5214),
    ("Sigma_b*-", 5114),
    ("anti-Sigma_b*-", -5224),
    # ("anti-Sigma_b*0", -5214),
    ("anti-Sigma_b*+", -5114),
)


@pytest.mark.parametrize("name,pid", decfile_style_names)
def test_decfile_style_names(name, pid):
    assert Particle.from_evtgen_name(name).pdgid == pid
