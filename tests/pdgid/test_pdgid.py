# Licensed under a 3-clause BSD style license, see LICENSE.

import pytest

from hepparticle.pdgid import PDGID


def test_class_methods():
    id = PDGID(11)
    assert id.pdgid == 11
    assert id.__str__() == '<PDGID: 11>'
    id = PDGID(-99999999)
    assert id.__str__() == '<PDGID: -99999999 (is_valid==False)>'
