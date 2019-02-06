# -*- coding: utf-8 -*-

import re
import math


def programmatic_name(name):
    'Return a name safe to use as a variable name.'
    name = re.sub('0$','_0',name)
    name = name if '~' not in name else ''.join(name.split('~'))+'_bar'
    return (name.replace(')(', '_').replace('(', '_').replace(')','')
                .replace('*', 'st').replace('\'','p')
                .replace('::', '_')
                .replace('/', '')
                .replace('--', '_mm').replace('++', '_pp')
                .replace('-', '_minus').replace('+', '_plus')
                .replace('~', 'bar'))


def str_with_unc(value, upper, lower=None):
    '''
    Utility to print out an uncertainty with different or
    identical upper/lower bounds. Nicely formats numbers using PDG rule.
    '''

    # Only bother with unicode if this is Python 3.
    pm = u'±' if type(u'') is type('') else '+/-'

    # If no lower passed, make them the same
    if lower is None:
        lower = upper

    # Uncertainties are always positive
    upper = abs(upper)
    lower = abs(lower)

    error = min(upper, lower)

    if error == 0:
        return str(value)

    value_digits = int(math.floor(math.log10(value)))
    error_digits = int(math.floor(math.log10(error) - math.log10(2.5)))
    pure_error_digits = int(math.floor(math.log10(error)))

    # This is split based on the value being larger than 1000000 or smaller than 0.001 - scientific notation split

    # This is normal notation
    if -3 < value_digits < 6:
        if error_digits < 0:
            fsv = fse = '.{0}f'.format(-error_digits)
        else:
            fsv = fse = '.0f'

    # This is scientific notation - a little odd, but better than the other options.
    else:
        fsv = '.{0}e'.format(abs(error_digits - value_digits))
        fse = '.0e' if error_digits == pure_error_digits else '.1e'


    # Now, print values based on upper=lower being true or not (even if they print the same)
    if upper == lower:
        return '{value:{fsv}} {pm} {upper:{fse}}'.format(value=value, pm=pm, upper=upper, fsv=fsv, fse=fse)
    else:
        return '{value:{fsv}} + {upper:{fse}} - {lower:{fse}}'.format(value=value,
                                                                      upper=upper, lower=lower,
                                                                      fsv=fsv, fse=fse)
