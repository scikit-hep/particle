# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Collection of enums to help characterising particle properties
Examples are charge, spin and parity.
"""

# Backport needed if Python 2 is used
try:
    from enum import IntEnum
except ImportError:
    from enum34 import IntEnum # Used in ZipApp


class SpinType(IntEnum):
    """
    Enum representing the spin type. Relevant only for bosons.

    SpinType.Unknown is returned for bosons if one of the values (J,P) is not known/relevant.
    SpinType.NonDefined is to be used for non-bosons.
    """
    #          Values of (J, P)
    Scalar = 1         # (0, 1)
    PseudoScalar = -1  # (0,-1)
    Vector = 2         # (1,-1)
    Axial = -2         # (1, 1)
    Tensor = 3         # (2, 1)
    PseudoTensor = -3  # (2,-1)
    Unknown = 0
    NonDefined = 5


class Parity(IntEnum):
    """Enum representing a particle parity."""
    p = 1
    o = 0
    m = -1
    u = 5


class Charge(IntEnum):
    """Enum representing the particle charge * 3."""
    pp = 6
    p = 3
    p23 = 2  # 2/3
    p13 = 1  # 1/3
    o = 0
    m13 = -1 # -1/3
    m23 = -2 # -2/3
    m = -3
    mm = -6
    u = 50


class Inv(IntEnum):
    """Enum defining what happens when a particle is inverted.

    Possible Values
    ---------------
        Same     : particle = antiparticle, e.g. pi0.
        Barred   : antiparticle is denoted with a bar, e.g. proton, Lambda.
                   Note that the charge may or may not be part of the name, e.g. Lb0 vs neutrinos.
        ChargeInv: antiparticle is obtained with a change of charge, e.g. pi+ vs pi-.
    """
    Same = 0
    Barred = 1
    ChargeInv = 2


class Status(IntEnum):
    'The status of the particle.'
    Common = 0
    Rare = 1
    Unsure = 2
    Further = 3
    Nonexistent = 4


# Mappings that allow the above classes to be produced from text mappings
Parity_mapping = {'+': Parity.p, '0': Parity.o, '-': Parity.m, '?': Parity.u, '': Parity.u}
Charge_mapping = {
    '++': Charge.pp, '+': Charge.p,
    '+2/3': Charge.p23, '+1/3': Charge.p13,
    '0': Charge.o,
    '-1/3': Charge.m13, '-2/3': Charge.m23,
    '-': Charge.m, '--': Charge.mm,
    '?': Charge.u, '': Charge.u}

Inv_mapping = {'': Inv.Same, 'F': Inv.Barred, 'B': Inv.ChargeInv}
Status_mapping = {'R': Status.Common, 'D': Status.Rare, 'S': Status.Unsure, 'F': Status.Further}

# Mappings that allow the above classes to be turned into text mappings
Parity_undo = {Parity.p: '+', Parity.o: '0', Parity.m: '-', Parity.u: '?'}
Parity_prog = {Parity.p: 'p', Parity.o: '0', Parity.m: 'm', Parity.u: 'u'}

Charge_undo = {Charge.pp: '++', Charge.p: '+',
               Charge.p23: '+2/3', Charge.p13: '+1/3',
               Charge.o: '0',
               Charge.m13: '-1/3', Charge.m23: '+2/3',
               Charge.m: '-', Charge.mm: '--',
               Charge.u: '?'}
Charge_prog = {Charge.pp: 'pp', Charge.p: 'p',
               Charge.p23: 'p23', Charge.p13: 'p13',
               Charge.o: '0',
               Charge.m13: 'm13', Charge.m23: 'm23',
               Charge.m: 'm', Charge.mm: 'mm',
               Charge.u: 'u'}
