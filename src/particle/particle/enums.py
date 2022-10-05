# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Collection of enums to help characterising particle properties
Examples are charge, spin and parity.
"""

from __future__ import annotations

from enum import IntEnum


class SpinType(IntEnum):
    """
    Enum representing the spin type. Relevant only for bosons.

    SpinType.Unknown is returned for bosons if one of the values (J,P) is not known/relevant.
    SpinType.NonDefined is to be used for non-bosons.
    """

    #          Values of (J, P)
    Scalar = 1  # (0, 1)
    PseudoScalar = -1  # (0,-1)
    Vector = 2  # (1,-1)
    Axial = -2  # (1, 1)
    Tensor = 3  # (2, 1)
    PseudoTensor = -3  # (2,-1)
    Unknown = 0
    NonDefined = 5


class Parity(IntEnum):
    """Enum representing a particle parity."""

    p = 1
    m = -1
    u = 5


class Charge(IntEnum):
    """Enum representing the particle charge * 3."""

    pp = 6
    p43 = 4  # 4/3
    p = 3
    p23 = 2  # 2/3
    p13 = 1  # 1/3
    o = 0
    m13 = -1  # -1/3
    m23 = -2  # -2/3
    m = -3
    m43 = -4  # -4/3
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
    """
    The status of the particle, a one-letter code used by the PDG
    e.g. in the extended particle data table (PDT), see our .fwf files.
    The meanings are reproduced here for completeness,
    see also the Status_mapping dictionary in this module.
    RPP stands for the (PDG) Review of Particle Properties.

    Possible Values
    ---------------
        Common   : extended PDT code "R" - established particle
                   in RPP Summary Table in Particle Physics Booklet
                   (established quarks, gauge bosons, leptons, mesons and baryons,
                   except those in D below).
        Rare     : extended PDT code "D" - the particle is omitted from the
                   Summary Tables in Particle Physics Booklet, but not from the Review.
                   These entries are omitted only to save space even though they are well established.
        Unsure   : extended PDT code "S" - the particle is omitted from the
                   particle properties Summary Tables because it is not well established.
        Further  : extended PDT code "F" - special case "Further mesons", see RPP.
                   These states are in the RPP database but are poorly established
                   or observed by a single group and thus need confirmation.
        NotInPDT : an extra code (empty string "") we here use for non-standard
                   and exotic particles not in the PDT.
    """

    Common = 0
    Rare = 1
    Unsure = 2
    Further = 3
    NotInPDT = 4


# Mappings that allow the above classes to be produced from text mappings
Parity_mapping = {
    "+": Parity.p,
    "-": Parity.m,
    "?": Parity.u,
    "": Parity.u,
}
Charge_mapping = {
    "++": Charge.pp,
    "+4/3": Charge.p43,
    "+": Charge.p,
    "+2/3": Charge.p23,
    "+1/3": Charge.p13,
    "0": Charge.o,
    "-1/3": Charge.m13,
    "-2/3": Charge.m23,
    "-": Charge.m,
    "-4/3": Charge.m43,
    "--": Charge.mm,
    "?": Charge.u,
    "": Charge.u,
}

Inv_mapping = {"": Inv.Same, "F": Inv.Barred, "B": Inv.ChargeInv}
Status_mapping = {
    "R": Status.Common,
    "D": Status.Rare,
    "S": Status.Unsure,
    "F": Status.Further,
    "": Status.NotInPDT,
}

# Mappings that allow the above classes to be turned into text mappings
Parity_undo = {Parity.p: "+", Parity.m: "-", Parity.u: "None"}
Parity_prog = {Parity.p: "p", Parity.m: "m", Parity.u: "u"}

Charge_undo = {
    Charge.pp: "++",
    Charge.p43: "+4/3",
    Charge.p: "+",
    Charge.p23: "+2/3",
    Charge.p13: "+1/3",
    Charge.o: "0",
    Charge.m13: "-1/3",
    Charge.m23: "-2/3",
    Charge.m: "-",
    Charge.m43: "-4/3",
    Charge.mm: "--",
    Charge.u: "None",
}
Charge_prog = {
    Charge.pp: "pp",
    Charge.p43: "p43",
    Charge.p: "p",
    Charge.p23: "p23",
    Charge.p13: "p13",
    Charge.o: "0",
    Charge.m13: "m13",
    Charge.m23: "m23",
    Charge.m: "m",
    Charge.m43: "m43",
    Charge.mm: "mm",
    Charge.u: "u",
}
