# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import pytest

from particle.geant import GeantID
from particle.pdgid import PDGID
from particle.exceptions import MatchingIDNotFound


def test_class_string_representations():
    pid = GeantID(1)
    assert pid == 1
    assert pid.__str__() == '<GeantID: 1>'


def test_class_return_type():
    assert isinstance(-GeantID(3), GeantID)
    assert isinstance(~GeantID(3), GeantID)


def test_class_inversion():
    assert -GeantID(1) == ~GeantID(1)


def test_from_pdgid():
    assert GeantID.from_pdgid(211) == 8

    assert GeantID.from_pdgid(PDGID(211)) == 8
    assert GeantID.from_pdgid(PDGID(211)) == GeantID(8)


def test_to_pdgid():
    geantid = GeantID(8)
    assert geantid.to_pdgid() == 211
    assert geantid.to_pdgid() == PDGID(211)
