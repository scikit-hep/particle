# -*- coding: utf-8 -*-

import math

def programmatic_name(name):
    'Return a name safe to use as a variable name'
    return (name.replace('(', '').replace(')', '')
            .replace('*', '').replace('::', '_')
            .replace('-', 'm').replace('+', 'p')
            .replace('~', 'bar'))


def mkul(upper, lower, numdig=''):
    'Utility to print out an uncertainty with different or identical upper/lower bounds'
    if upper == lower:
        if upper == 0:
            return u''
        else:
            return u'± {upper:{numdig}f}'.format(upper=upper, numdig=numdig)
    else:
        return u'+ {upper:{numdig}f} - {lower:{numdig}f}'.format(upper=upper, lower=lower, numdig=numdig)

    
def str_with_unc(value, upper, lower):
    'Utility to nicely display a value with unc'
    
    err = min(upper, lower)

    if 0 < err < 2.5:
        numdig = u'.' + str(math.ceil(-math.log10(err) + math.log10(2.5)))
    elif err >= 2.5:
        numdig = u'.0'
    else:
        numdig = u''
    
    ending = mkul(upper, lower, numdig)
    if ending:
        ending = u' ' + ending
    return u'{value:{numdig}f}{ending}'.format(value=value, ending=ending, numdig=numdig)
