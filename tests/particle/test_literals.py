# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import division

import pytest

from particle.particle import literals as lp


def test_literals_import():
    assert lp is not None
