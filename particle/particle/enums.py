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


class Par(IntEnum):
    'Represents parity or charge'
    pp = 2
    p = 1
    o = 0
    m = -1
    mm = -2
    u = 5


Charge = Par


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
Par_mapping = {'+': Par.p, '0': Par.o, '+2/3': Par.u,
               '++': Par.pp, '-': Par.m, '-1/3': Par.u, '?': Par.u, '': Par.o}
Inv_mapping = {'': Inv.Same, 'F': Inv.Full, 'B': Inv.Barless}
Status_mapping = {'R': Status.Common, 'D': Status.Rare, 'S': Status.Unsure, 'F': Status.Further}

# Mappings that allow the above classes to be turned into text mappings
Par_undo = {Par.pp: '++', Par.p: '+', Par.o: '0', Par.m: '-', Par.mm: '--', Par.u: '?'}
Par_prog = {Par.pp: 'pp', Par.p: 'p', Par.o: '0', Par.m: 'm', Par.mm: 'mm', Par.u: 'u'}

