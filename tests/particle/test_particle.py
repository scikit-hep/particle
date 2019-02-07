# -*- encoding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import sys

import pytest
from pytest import approx

from particle.particle.enums import Charge, SpinType
from particle.particle import Particle
from particle.particle.particle import ParticleNotFound, InvalidParticle
from particle.pdgid import PDGID

from hepunits.units import second

def test_enums_Charge():
    assert Charge.p + Charge.m == Charge.o
    assert Charge.pp + Charge.mm == Charge.o


def test_enums_SpinType():
    assert SpinType.PseudoScalar == - SpinType.Scalar
    assert SpinType.Axial == - SpinType.Vector
    assert SpinType.PseudoTensor == - SpinType.Tensor


def test_from_search():
    # 1 match found
    prepr = repr(Particle.from_search(name='gamma'))
    assert prepr == "<Particle: pdgid=22, fullname='gamma', mass=0.0 MeV>"

    # No match found
    with pytest.raises(ParticleNotFound):
        Particle.from_search(name='NonExistent')

    # Multiple matches found
    with pytest.raises(RuntimeError):
        Particle.from_search(name=lambda x: 'Upsilon' in x)

def test_lambda_style_search():
    particles = Particle.from_search_list(lambda p: p.name == 'p')
    assert len(particles) == 2
    assert 2212 in particles
    assert -2212 in particles

    assert Particle.from_search(lambda p: p.name == 'p' and p > 0) == 2212
    assert Particle.from_search(lambda p: p.name == 'p' and p < 0) == -2212

def test_fuzzy_name_search():
    particles = Particle.from_search_list('p~')
    assert len(particles) == 1
    assert -2212 in particles

def test_keyword_style_search():
    particles = Particle.from_search_list(name = 'p')
    assert len(particles) == 2
    assert 2212 in particles
    assert -2212 in particles

    assert Particle.from_search(name = 'p', particle=True) == 2212
    assert Particle.from_search(name = 'p', particle=False) == -2212

def test_keyword_lambda_style_search():
    particles = Particle.from_search_list(name = lambda x: 'p' == x)
    assert len(particles) == 2
    assert 2212 in particles
    assert -2212 in particles

    # Fuzzy name
    particles = Particle.from_search_list(name = lambda x: 'p' in x)
    assert len(particles) > 2
    assert 2212 in particles
    assert -2212 in particles

    # Name and particle
    assert Particle.from_search(name = lambda x: x == 'p', particle=True) == 2212

    # Unit based comparison
    assert 2212 in Particle.from_search_list(lifetime = lambda x : x > 1*second)

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
    assert "fullname='pi+'" in repr(pi)
    assert "mass=139.57" in repr(pi)


def test_basic_props():
    pi = Particle.from_pdgid(211)
    assert pi.name == 'pi'
    assert pi.pdgid == 211
    assert pi.three_charge == Charge.p


def test_lifetime_props():
    pi = Particle.from_pdgid(211)
    assert pi.lifetime == approx(26.0327460625985)   # in nanoseconds
    assert pi.ctau == approx(7804.4209306)   # in millimeters


def test_describe():
    __description = u'Lifetime = 26.033 ± 0.005 ns'
    if sys.version_info < (3, 0):
        __description = __description.replace(u'±', u'+/-')
    pi = Particle.from_pdgid(211)
    assert __description in pi.describe()

    __description = r"""Name: gamma      ID: 22           Fullname: gamma          Latex: $\gamma$
Mass  = 0.0 MeV
Width = 0.0 MeV
I (isospin)       = <2     G (parity)        = 0      Q (charge)       = 0
J (total angular) = 1.0    C (charge parity) = ?      P (space parity) = ?
    Antiparticle status: Same (antiparticle name: gamma)"""
    photon = Particle.from_pdgid(22)
    assert photon.describe() == __description

    __description = 'Width = 1.89 + 0.09 - 0.18 MeV'
    Sigma_c_pp = Particle.from_pdgid(4222)
    assert __description in Sigma_c_pp.describe()


ampgen_style_names = (
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
    ("anti-K*0", -313),
    ("a_1(1260)+", 20213),
    # "D'_1+"
    # "D_2*+"
)


@pytest.mark.parametrize("name,pid", decfile_style_names)
def test_decfile_style_names(name, pid):
    assert Particle.from_dec(name).pdgid == pid
