# -*- coding: utf-8 -*-

import pytest
import sys

from particle.particle.utilities import str_with_unc

def test_unc_printout():
    pm = '+/-' if sys.version_info < (3,0) else '±'
    
    assert str_with_unc(1234.5, .03, .03) == '1234.50 {pm} 0.03'.format(pm=pm)
    assert str_with_unc(.00001231, .000002, .000004) == '0.0000123 + 0.0000020 - 0.0000040'
    assert str_with_unc(1234.5, 5, 5) == '1234 {pm} 5'.format(pm=pm)
    assert str_with_unc(1234.5, 2, 2) == '1234.5 {pm} 2.0'.format(pm=pm)
