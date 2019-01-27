# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import division

import pytest

from particle.pdgid import literals as lid


def test_literals_import():
    assert lid is not None
