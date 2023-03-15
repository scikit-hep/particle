from __future__ import annotations

from sys import version_info

import pytest

import particle

python37plus_only = pytest.mark.skipif(
    version_info < (3, 7), reason="requires Python3.7+"
)


@python37plus_only
def test_top_level_api():
    assert dir(particle) == [
        "Charge",
        "Corsika7ID",
        "Geant3ID",
        "Inv",
        "InvalidParticle",
        "PDGID",
        "Parity",
        "Particle",
        "ParticleNotFound",
        "PythiaID",
        "SpinType",
        "Status",
        "__version__",
        "latex_to_html_name",
        "lifetime_to_width",
        "width_to_lifetime",
    ]


@python37plus_only
def test_api_converters():
    assert dir(particle.converters) == [
        "Corsika72PDGIDBiMap",
        "EvtGen2PDGNameMap",
        "EvtGenName2PDGIDBiMap",
        "Geant2PDGIDBiMap",
        "PDG2EvtGenNameMap",
        "Pythia2PDGIDBiMap",
    ]


@python37plus_only
def test_api_corsika():
    assert dir(particle.corsika) == ["Corsika7ID"]


@python37plus_only
def test_api_data():
    assert dir(particle.data) == ["basepath"]


@python37plus_only
def test_api_geant():
    assert dir(particle.geant) == ["Geant3ID"]


@python37plus_only
def test_api_lhcb():
    assert dir(particle.lhcb) == [
        "LHCbName2PDGIDBiMap",
        "from_lhcb_name",
        "to_lhcb_name",
    ]


@python37plus_only
def test_api_lhcb_data():
    assert dir(particle.lhcb.data) == ["basepath"]


@python37plus_only
def test_api_particle():
    assert dir(particle.particle) == [
        "Charge",
        "Inv",
        "InvalidParticle",
        "Parity",
        "Particle",
        "ParticleNotFound",
        "SpinType",
        "Status",
        "latex_name_unicode",
        "latex_to_html_name",
        "lifetime_to_width",
        "programmatic_name",
        "width_to_lifetime",
    ]


@python37plus_only
def test_api_pdgid():
    assert dir(particle.pdgid) == sorted(
        [
            "PDGID",
            #
            "is_valid",
            "abspid",
            # #
            "is_Qball",
            "is_Rhadron",
            "is_SUSY",
            "is_baryon",
            "is_diquark",
            "is_dyon",
            "is_excited_quark_or_lepton",
            "is_gauge_boson_or_higgs",
            "is_generator_specific",
            "is_hadron",
            "is_lepton",
            "is_meson",
            "is_nucleus",
            "is_pentaquark",
            "is_quark",
            "is_sm_gauge_boson_or_higgs",
            "is_sm_lepton",
            "is_sm_quark",
            "is_special_particle",
            "is_technicolor",
            #
            "has_down",
            "has_up",
            "has_strange",
            "has_charm",
            "has_bottom",
            "has_top",
            "has_fundamental_anti",
            #
            "charge",
            "three_charge",
            "j_spin",
            "J",
            "s_spin",
            "S",
            "l_spin",
            "L",
            "A",
            "Z",
        ]
    )


@python37plus_only
def test_api_pythia():
    assert dir(particle.pythia) == ["PythiaID"]
