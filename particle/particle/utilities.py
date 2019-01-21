# -*- coding: utf-8 -*-

def programmatic_name(name):
    'Return a name safe to use as a variable name'
    return (name.replace('(', '').replace(')', '')
            .replace('*', '').replace('::', '_')
            .replace('-', 'm').replace('+', 'p')
            .replace('~', 'bar'))


def mkul(upper, lower):
    'Utility to print out an uncertainty with different or identical upper/lower bounds'
    if upper == lower:
        if upper == 0:
            return u''
        else:
            return u'± {upper:g}'.format(upper=upper)
    else:
        return '+ {upper:g} - {lower:g}'.format(upper=upper, lower=lower)
