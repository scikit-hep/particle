

from particle.particle.utilities import str_with_unc

def test_unc_printout():
    assert str_with_unc(1234.5, .03, .03) == u'1234.50 ± 0.03'
    assert str_with_unc(.00001231, .000002, .000004) == u'0.0000123 + 0.0000020 - 0.0000040'
    assert str_with_unc(1234.5, 5, 5) == u'1234 ± 5'
    assert str_with_unc(1234.5, 2, 2) == u'1234.5 ± 2.0'