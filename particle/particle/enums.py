# Backport needed if Python 2 is used
from enum import IntEnum


class SpinType(IntEnum):
    'The spin type of a particle'
    Scalar = 1  # (0, 1)
    PseudoScalar = -1  # (0,-1)
    Vector = 2  # (1,-1)
    Axial = -2  # (1, 1)
    Tensor = 3  # (2, 1)
    PseudoTensor = -3  # (2,-1)
    Unknown = 0  # (0, 0)


class Parity(IntEnum):
    'Represents parity'
    p = 1
    o = 0
    m = -1
    u = 5


class Charge(IntEnum):
    'Represents charge * 3'
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
    'Definition of what happens when particle is inverted'
    Same = 0
    Full = 1
    Barless = 2


class Status(IntEnum):
    'The status of the particle'
    Common = 0
    Rare = 1
    Unsure = 2
    Further = 3
    Nonexistant = 4


# Mappings that allow the above classes to be produced from text mappings
Parity_mapping = {'+': Parity.p, '0': Parity.o, '-': Parity.u, '?': Parity.u, '': Parity.o}
Charge_mapping = {'+': Charge.p, '0': Charge.o, '+2/3': Charge.p23,
               '++': Charge.pp, '-': Charge.m, '-1/3': Charge.m13, '?': Charge.u, '': Charge.o}
Inv_mapping = {'': Inv.Same, 'F': Inv.Full, 'B': Inv.Barless}
Status_mapping = {'R': Status.Common, 'D': Status.Rare, 'S': Status.Unsure, 'F': Status.Further}

# Mappings that allow the above classes to be turned into text mappings
Parity_undo = {Parity.p: '+', Parity.o: '0', Parity.m: '-', Parity.u: '?'}
Parity_prog = {Parity.p: 'p', Parity.o: '0', Parity.m: 'm', Parity.u: 'u'}

Charge_undo = {Charge.pp: '++', Charge.p: '+', Charge.p23: '+2/3', Charge.p13: '+1/3',
               Charge.o: '0',  Charge.m13: '-1/3', Charge.m23: '+2/3',
               Charge.m: '-', Charge.mm: '--', Charge.u: '?'}
Charge_prog = {Charge.pp: 'pp', Charge.p: 'p', Charge.p23: 'p23', Charge.p13: 'p13',
               Charge.o: '0',  Charge.m13: 'm13', Charge.m23: 'm23',
               Charge.m: 'm', Charge.mm: 'mm', Charge.u: 'u'}
