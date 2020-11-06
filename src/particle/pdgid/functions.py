# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
The Particle Data Group (PDG) defines the standard particle identification numbering scheme
in the form of a signed 7-digit number +/- N Nr Nl Nq1 Nq2 Nq3 Nj.

PDG IDs with more than 7 digits exist for non-standard particles such as Q-balls.
These follow outside the standard PDG numbering scheme.

This module provides the following:

- A pythonic version of the functions defined in HepPID and HepPDT,
  which work with PDG particle identification codes (PDG IDs).
- A few other functions extending the functionality of the HepXXX code.

References
----------

- PDG document "Monte Carlo Particle Numbering Scheme".
- HepPDT and HepPID versions 3.04.01.
"""

from __future__ import print_function, division, absolute_import

from enum import IntEnum
from typing import SupportsInt, Optional

PDGID_TYPE = SupportsInt


class Location(IntEnum):
    """
    Represents the location digit in the PDG numbering scheme, which provides a convenient index into the PID.
    """

    Nj = 1
    Nq3 = 2
    Nq2 = 3
    Nq1 = 4
    Nl = 5
    Nr = 6
    N = 7
    N8 = 8
    N9 = 9
    N10 = 10


def is_valid(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Is it a valid PDG ID?"""
    if _fundamental_id(pdgid) != 0:  # function always returns a number >= 0
        return True
    if is_meson(pdgid):
        return True
    if is_baryon(pdgid):
        return True
    if is_gauge_boson_or_higgs(pdgid):
        return True
    if is_pentaquark(pdgid):
        return True
    if is_SUSY(pdgid):
        return True
    if is_Rhadron(pdgid):
        return True
    if is_dyon(pdgid):
        return True
    if is_diquark(pdgid):
        return True
    if is_pentaquark(pdgid):
        return True
    if is_generator_specific(pdgid):
        return True
    if is_technicolor(pdgid):
        return True
    if is_composite_quark_or_lepton(pdgid):
        return True
    if _extra_bits(pdgid) > 0:
        return is_Qball(pdgid) or is_nucleus(pdgid)
    return False


def abspid(pdgid):
    # type: (PDGID_TYPE) -> int
    """Returns the absolute value of the PDG ID."""
    return abs(int(pdgid))


def is_quark(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a quark?

    Fourth-generation quarks are included, but not excited (composite) quarks.
    """
    return 1 <= abspid(pdgid) <= 8


def is_lepton(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this PDG ID correspond to a lepton?"""
    if _extra_bits(pdgid) > 0:
        return False
    if 11 <= int(_fundamental_id(pdgid)) <= 18:
        return True
    return False


def is_hadron(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this PDG ID correspond to a hadron?"""
    # Special case of proton and neutron:
    # needs to be checked first since _extra_bits(pdgid) > 0 for nuclei
    if abs(int(pdgid)) in {1000000010, 1000010010}:
        return True
    if _extra_bits(pdgid) > 0:
        return False
    if is_meson(pdgid):
        return True
    if is_baryon(pdgid):
        return True
    if is_pentaquark(pdgid):
        return True
    if is_Rhadron(pdgid):
        return True
    return False


def is_meson(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this PDG ID correspond to a meson?"""
    if _extra_bits(pdgid) > 0:
        return False
    if abspid(pdgid) <= 100:
        return False
    if 0 < int(_fundamental_id(pdgid)) <= 100:
        return False
    # Special IDs - K(L)0, ???, K(S)0
    if abspid(pdgid) in {130, 210, 310}:
        return True
    # Special IDs - B(L)0, B(sL)0, B(H)0, B(sH)0
    if abspid(pdgid) in {150, 350, 510, 530}:
        return True
    # Special particles - reggeon, pomeron, odderon
    if int(pdgid) in {110, 990, 9990}:
        return True
    if (
        _digit(pdgid, Location.Nj) > 0
        and _digit(pdgid, Location.Nq3) > 0
        and _digit(pdgid, Location.Nq2) > 0
        and _digit(pdgid, Location.Nq1) == 0
    ):
        # check for illegal antiparticles
        if (
            _digit(pdgid, Location.Nq3) == _digit(pdgid, Location.Nq2)
            and int(pdgid) < 0
        ):
            return False
        else:
            return True
    return False


def is_baryon(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this PDG ID correspond to a baryon?"""
    if abspid(pdgid) <= 100:
        return False
    # Special case of proton and neutron:
    # needs to be checked first since _extra_bits(pdgid) > 0 for nuclei
    if abs(int(pdgid)) in {1000000010, 1000010010}:
        return True

    if _extra_bits(pdgid) > 0:
        return False

    if 0 < _fundamental_id(pdgid) <= 100:
        return False

    # Old codes for diffractive p and n (MC usage)
    if abspid(pdgid) in {2110, 2210}:
        return True

    if (
        _digit(pdgid, Location.Nj) > 0
        and _digit(pdgid, Location.Nq3) > 0
        and _digit(pdgid, Location.Nq2) > 0
        and _digit(pdgid, Location.Nq1) > 0
    ):
        return True

    if is_Rhadron(pdgid) or is_pentaquark(pdgid):
        return False

    return False


def is_diquark(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this PDG ID correspond to a diquark?"""
    if _extra_bits(pdgid) > 0:
        return False
    if abspid(pdgid) <= 100:
        return False
    if 0 < int(_fundamental_id(pdgid)) <= 100:
        return False
    if (
        _digit(pdgid, Location.Nj) > 0
        and _digit(pdgid, Location.Nq3) == 0
        and _digit(pdgid, Location.Nq2) > 0
        and _digit(pdgid, Location.Nq1) > 0
    ):
        return True
    return False


def is_nucleus(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a nucleus?

    Ion numbers are +/- 10LZZZAAAI.
    AAA is A - total baryon number
    ZZZ is Z - total charge
    L is the total number of strange quarks.
    I is the isomer number, with I=0 corresponding to the ground state.
    """
    # A proton can be a Hydrogen nucleus
    # A neutron can be considered as a nucleus when given the PDG ID 1000000010,
    # hence consistency demands that is_nucleus(neutron) is True
    if abspid(pdgid) in {2112, 2212}:
        return True
    if _digit(pdgid, Location.N10) == 1 and _digit(pdgid, Location.N9) == 0:
        # Charge should always be less than or equal to the baryon number
        A_pdgid = A(pdgid)
        Z_pdgid = Z(pdgid)

        if A_pdgid is None or Z_pdgid is None:
            return False
        elif A_pdgid >= abs(Z_pdgid):
            return True
    return False


def is_pentaquark(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does the PDG ID correspond to a pentaquark?

    Pentaquark IDs are of the form +/- 9 Nr Nl Nq1 Nq2 Nq3 Nj, where Nj = 2J + 1 gives the spin
    and Nr Nl Nq1 Nq2 Nq3 denote the quark numbers in order Nr >= Nl >= Nq1 >= Nq2
    and Nq3 gives the antiquark number.
    """
    if _extra_bits(pdgid) > 0:
        return False
    if _digit(pdgid, Location.N) != 9:
        return False
    if _digit(pdgid, Location.Nr) == 9 or _digit(pdgid, Location.Nr) == 0:
        return False
    if _digit(pdgid, Location.Nj) == 9 or _digit(pdgid, Location.Nl) == 0:
        return False
    if _digit(pdgid, Location.Nq1) == 0:
        return False
    if _digit(pdgid, Location.Nq2) == 0:
        return False
    if _digit(pdgid, Location.Nq3) == 0:
        return False
    if _digit(pdgid, Location.Nj) == 0:
        return False
    if _digit(pdgid, Location.Nq2) > _digit(pdgid, Location.Nq1):
        return False
    if _digit(pdgid, Location.Nq1) > _digit(pdgid, Location.Nl):
        return False
    if _digit(pdgid, Location.Nl) > _digit(pdgid, Location.Nr):
        return False
    return True


def is_gauge_boson_or_higgs(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a gauge boson or a Higgs?

    Codes 21-30 are reserved for the Standard Model gauge bosons and the Higgs.
    The graviton and the boson content of a two-Higgs-doublet scenario
    and of additional SU(2)xU(1) groups are found in the range 31-40.
    """
    return True if 21 <= abspid(pdgid) <= 40 else False


def is_sm_gauge_boson_or_higgs(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a Standard Model gauge boson or Higgs?

    Codes 21-30 are reserved for the Standard Model gauge bosons and the Higgs,
    but only the codes 21-25 actually correspond to SM particles.
    """
    if abspid(pdgid) == 24:  # W is the only SM gauge boson not its antiparticle
        return True

    return True if 21 <= int(pdgid) <= 25 else False


def is_generator_specific(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to generator-specific pseudoparticles or concepts?

    Codes 81-100 are reserved for generator-specific pseudoparticles and concepts.
    Codes 901-930, 1901-1930, 2901-2930, and 3901-3930 are for
    additional components of Standard Model parton distribution functions,
    where the latter three ranges are intended to distinguish
    left/right/longitudinal components.
    Codes 998 and 999 are reserved for GEANT tracking purposes.
    """
    aid = abspid(pdgid)
    if 81 <= aid <= 100:
        return True
    if 901 <= aid <= 930:
        return True
    if 1901 <= aid <= 1930:
        return True
    if 2901 <= aid <= 2930:
        return True
    if 3901 <= aid <= 3930:
        return True
    if aid in {998, 999}:
        return True
    if aid in {20022, 480000000}:  # Special cases of opticalphoton and geantino
        return True
    return False


def is_special_particle(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a special particle?

    Special particle in the sense of the classification in the PDG MC particle numbering scheme document,
    hence the graviton, the DM (S = 0, 1/2, 1) particles, the reggeons (reggeon, pomeron and odderon),
    and all generator-specific pseudo-particles and concepts, see `is_generator_specific`.
    """
    return pdgid in {39, 41, 42, 51, 52, 53, 110, 990, 9990} or is_generator_specific(
        pdgid
    )


def is_Rhadron(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to an R-hadron?

    An R-hadron is of the form 10abcdj, 100abcj, or 1000abj,
    where j = 2J + 1 gives the spin; b, c, and d are quarks or gluons;
    and a (the digit following the zero's) is a SUSY particle.
    """
    if _extra_bits(pdgid) > 0:
        return False
    if _digit(pdgid, Location.N) != 1:
        return False
    if _digit(pdgid, Location.Nr) != 0:
        return False
    if is_SUSY(pdgid):
        return False
    # All R-hadrons have at least 3 core digits
    if (
        _digit(pdgid, Location.Nq2) == 0
        or _digit(pdgid, Location.Nq3) == 0
        or _digit(pdgid, Location.Nj) == 0
    ):
        return False
    return True


def is_Qball(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a Q-ball or any exotic particle with electric charge beyond the qqq scheme?

    Ad-hoc numbering for such particles is +/- 100XXXY0, where XXX.Y is the charge.
    """
    if _extra_bits(pdgid) != 1:
        return False
    if _digit(pdgid, Location.N) != 0:
        return False
    if _digit(pdgid, Location.Nr) != 0:
        return False
    if (abspid(pdgid) // 10) % 10000 == 0:
        return False
    if _digit(pdgid, Location.Nj) != 0:
        return False
    return True


def is_dyon(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a Dyon, a magnetic monopole?

    Magnetic monopoles and Dyons are assumed to have one unit of Dirac monopole charge
    and a variable integer number xyz units of electric charge,
    where xyz stands for Nq1 Nq2 Nq3.

    Codes 411xyz0 are used when the magnetic and electrical charge sign agree and 412xyz0 when they disagree,
    with the overall sign of the particle set by the magnetic charge.
    For now, no spin information is provided.
    """
    if _extra_bits(pdgid) > 0:
        return False
    if _digit(pdgid, Location.N) != 4:
        return False
    if _digit(pdgid, Location.Nr) != 1:
        return False
    if _digit(pdgid, Location.Nl) not in {1, 2}:
        return False
    if _digit(pdgid, Location.Nq3) == 0:
        return False
    if _digit(pdgid, Location.Nj) != 0:
        return False
    return True


def is_SUSY(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a SUSY particle?

    Fundamental SUSY particles have N = 1 or 2.
    """
    if _extra_bits(pdgid) > 0:
        return False
    if _digit(pdgid, Location.N) != 1 and _digit(pdgid, Location.N) != 2:
        return False
    if _digit(pdgid, Location.Nr) != 0:
        return False
    if _fundamental_id(pdgid) == 0:
        return False
    return True


def is_technicolor(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to a Technicolor state?

    Technicolor states have N = 3.
    """
    if _extra_bits(pdgid) > 0:
        return False
    return True if _digit(pdgid, Location.N) == 3 else False


def is_composite_quark_or_lepton(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    Does this PDG ID correspond to an excited (composite) quark or lepton?

    Excited (composite) quarks and leptons have N = 4 and Nr = 0.
    """
    if _extra_bits(pdgid) > 0:
        return False
    if _fundamental_id(pdgid) == 0:
        return False
    if not (_digit(pdgid, Location.N) == 4 and _digit(pdgid, Location.Nr) == 0):
        return False
    return True


def has_down(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this particle contain a down quark?"""
    return _has_quark_q(pdgid, 1)


def has_up(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this particle contain an up quark?"""
    return _has_quark_q(pdgid, 2)


def has_strange(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this particle contain a strange quark?"""
    return _has_quark_q(pdgid, 3)


def has_charm(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this particle contain a charm quark?"""
    return _has_quark_q(pdgid, 4)


def has_bottom(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this particle contain a bottom quark?"""
    return _has_quark_q(pdgid, 5)


def has_top(pdgid):
    # type: (PDGID_TYPE) -> bool
    """Does this particle contain a top quark?"""
    return _has_quark_q(pdgid, 6)


def has_fundamental_anti(pdgid):
    # type: (PDGID_TYPE) -> bool
    """
    If this is a fundamental particle, does it have a valid antiparticle?

    Notes
    -----
    Based on the current list of defined particles/concepts
    in the PDG Monte Carlo Particle Numbering Scheme document.
    """
    fid = _fundamental_id(pdgid)  # always a positive integer

    # Check generator-specific PDGIDs
    if 81 <= fid <= 100:
        return True if fid in {82, 84, 85, 86, 87} else False

    # Check PDGIDs from 1 to 79
    _cp_conjugates = {21, 22, 23, 25, 32, 33, 35, 36, 39, 40, 43}
    _unassigned = (
        [9, 10, 19, 20, 26] + list(range(26, 32)) + list(range(45, 80))
    )  # not in conversion.csv
    if (1 <= fid <= 79) and fid not in _cp_conjugates:
        return False if fid in _unassigned else True

    return False


def charge(pdgid):
    # type: (PDGID_TYPE) -> Optional[float]
    """Returns the charge."""

    three_charge_pdgid = three_charge(pdgid)
    if three_charge_pdgid is None:
        return None
    elif not is_Qball(pdgid):
        return three_charge_pdgid / 3.0
    else:
        return three_charge_pdgid / 30.0


def three_charge(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """
    Returns 3 times the charge.

    None is returned if the PDGID is not valid.
    """
    if not is_valid(pdgid):
        return None

    aid = abspid(pdgid)
    charge = None
    ch100 = [
        -1,
        2,
        -1,
        2,
        -1,
        2,
        -1,
        2,
        0,
        0,
        -3,
        0,
        -3,
        0,
        -3,
        0,
        -3,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        3,
        0,
        0,
        3,
        0,
        0,
        0,
        0,
        -1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        6,
        3,
        6,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    q1 = _digit(pdgid, Location.Nq1)
    q2 = _digit(pdgid, Location.Nq2)
    q3 = _digit(pdgid, Location.Nq3)
    sid = _fundamental_id(pdgid)

    if _extra_bits(pdgid) > 0:
        if is_nucleus(pdgid):  # ion
            Z_pdgid = Z(pdgid)
            if Z_pdgid is None:
                return None
            else:
                return 3 * Z_pdgid
        elif is_Qball(pdgid):  # Qball
            charge = 3 * ((aid // 10) % 10000)
        else:  # this should never be reached in the present numbering scheme
            return None  # since extra bits exist only for Q-balls and nuclei
    elif is_dyon(pdgid):  # Dyon
        charge = 3 * ((aid // 10) % 1000)
        # this is half right
        # the charge sign will be changed below if pid < 0
        if _digit(pdgid, Location.Nl) == 2:
            charge = -charge
    elif 0 < sid <= 100:  # use table
        charge = ch100[sid - 1]
        if aid in {1000017, 1000018, 1000034, 1000052, 1000053, 1000054}:
            charge = 0
        if aid == 5100061 or aid == 5100062:
            charge = 6
    elif _digit(pdgid, Location.Nj) == 0:  # KL, KS, or undefined
        return 0
    elif q1 == 0 or (is_Rhadron(pdgid) and q1 == 9):  # mesons
        if q2 == 3 or q2 == 5:
            charge = ch100[q3 - 1] - ch100[q2 - 1]
        else:
            charge = ch100[q2 - 1] - ch100[q3 - 1]
    elif q3 == 0:  # diquarks
        charge = ch100[q2 - 1] + ch100[q1 - 1]
    elif is_baryon(pdgid) or (
        is_Rhadron(pdgid) and _digit(pdgid, Location.Nl) == 9
    ):  # baryons
        charge = ch100[q3 - 1] + ch100[q2 - 1] + ch100[q1 - 1]

    if charge is not None and int(pdgid) < 0:
        charge = -charge
    return charge


def j_spin(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """Returns the total spin as 2J+1."""
    if not is_valid(pdgid):
        return None
    if _fundamental_id(pdgid) > 0:
        fund = _fundamental_id(pdgid)
        if 0 < fund < 7:
            return 2  # 4th generation quarks not dealt with !
        if fund == 9:
            return 3
        if 10 < fund < 17:
            return 2  # 4th generation leptons not dealt with !
        if 20 < fund < 25:
            return 3
        return None
    elif abs(int(pdgid)) in {1000000010, 1000010010}:  # neutron, proton
        return 2
    elif _extra_bits(pdgid) > 0:
        return None
    if pdgid in {130, 310}:
        return 1  # Special cases of the KS and KL !
    return abspid(pdgid) % 10


def J(pdgid):
    # type: (PDGID_TYPE) -> Optional[float]
    """Returns the total spin J."""
    value = j_spin(pdgid)
    return (
        (value - 1) / 2 if value is not None else value
    )  # This works due to the Python 3 style division


def S(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """
    Returns the spin S.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    if not is_meson(pdgid):
        return None

    if not is_valid(pdgid):
        return None

    if (abspid(pdgid) // 1000000) % 10 == 9:
        return None  # no knowledge so far

    nl = (abspid(pdgid) // 10000) % 10
    js = abspid(pdgid) % 10

    if not (js == 1 or js >= 3):
        return 0

    if nl == 0:
        return 0 if js == 1 else 1
    elif nl == 1:
        return 1 if js == 1 else 0
    elif nl in {2, 3}:
        return 1 if js >= 3 else 0
    else:
        return 0


def s_spin(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """
    Returns the spin S as 2S+1.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    value = S(pdgid)
    return (2 * value + 1) if value is not None else value


def L(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """
    Returns the orbital angular momentum L.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    if not is_meson(pdgid):
        return None

    if not is_valid(pdgid):
        return None

    if (abspid(pdgid) // 1000000) % 10 == 9:
        return None  # no knowledge so far

    nl = (abspid(pdgid) // 10000) % 10
    js = abspid(pdgid) % 10

    if nl == 0:
        if js == 1:
            return 0
        if js == 3:
            return 0
        if js == 5:
            return 1
        if js == 7:
            return 2
        if js == 9:
            return 3
    elif nl == 1:
        if js == 1:
            return 1
        if js == 3:
            return 1
        if js == 5:
            return 2
        if js == 7:
            return 3
        if js == 9:
            return 4
    elif nl == 2:
        if js == 3:
            return 1
        if js == 5:
            return 2
        if js == 7:
            return 3
        if js == 9:
            return 4
    elif nl == 3:
        if js == 3:
            return 2
        if js == 5:
            return 3
        if js == 7:
            return 4
        if js == 9:
            return 5

    return 0


def l_spin(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """
    Returns the orbital angular momentum L as 2L+1.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    value = L(pdgid)
    return (2 * value + 1) if value is not None else value


def A(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """Returns the atomic number A if the PDG ID corresponds to a nucleus. Else it returns None."""
    # A proton can be a Hydrogen nucleus
    # A neutron can be considered as a nucleus when given the PDG ID 1000000010,
    # hence consistency demands that A(neutron) = 1
    if abspid(pdgid) in {2112, 2212}:
        return 1
    if _digit(pdgid, Location.N10) != 1 or _digit(pdgid, Location.N9) != 0:
        return None
    return (abspid(pdgid) // 10) % 1000


def Z(pdgid):
    # type: (PDGID_TYPE) -> Optional[int]
    """Returns the charge Z if the PDG ID corresponds to a nucleus. Else it returns None."""
    # A proton can be a Hydrogen nucleus
    if abspid(pdgid) == 2212:
        return int(pdgid) // 2212
    # A neutron can be considered as a nucleus when given the PDG ID 1000000010,
    # hence consistency demands that Z(neutron) = 0
    if abspid(pdgid) == 2112:
        return 0
    if _digit(pdgid, Location.N10) != 1 or _digit(pdgid, Location.N9) != 0:
        return None
    return ((abspid(pdgid) // 10000) % 1000) * (int(pdgid) // abs(int(pdgid)))


def _digit(pdgid, loc):
    # type: (PDGID_TYPE, int) -> int
    """
    Provides a convenient index into the PDGID number, whose format is in base 10.

    Returns the digit at position 'loc' given that the right-most digit is at position 1.
    """
    sid = str(abspid(pdgid))
    return int(sid[-loc]) if loc <= len(sid) else 0


def _extra_bits(pdgid):
    # type: (PDGID_TYPE) -> int
    """
    Returns everything beyond the 7th digit, so anything outside the PDG numbering scheme.
    """
    return abspid(pdgid) // 10000000


def _fundamental_id(pdgid):
    # type: (PDGID_TYPE) -> int
    """
    Returns the first 2 digits if this is a "fundamental" particle.
    Returns 0 if the particle is not fundamental or not standard (PDG ID with more than 7 digits).

    PDGID=100 is a special case (internal generator ID's are 81-100).

    Notes
    -----
    Function always returns a number >= 0.
    """
    if _extra_bits(pdgid) > 0:
        return 0
    if _digit(pdgid, Location.Nq2) == 0 and _digit(pdgid, Location.Nq1) == 0:
        return abspid(pdgid) % 10000
    elif abspid(pdgid) <= 100:
        return abspid(pdgid)
    else:
        return 0


def _has_quark_q(pdgid, q):
    # type: (PDGID_TYPE, int) -> bool
    """
    Helper function - does this particle contain a quark q?

    Note that q is always positive, so [1, 6] for Standard Model quarks
    and [7, 8] for fourth-generation quarks.
    """
    # Nuclei can also contain strange quarks,
    # cf. the definition of a nucleus PDG ID in is_nucleus.
    # This check needs to be done first since _extra_bits(pdgid) > 0 for nuclei
    if is_nucleus(pdgid):
        if q in {1, 2}:
            return True  # Nuclei by construction contain up and down quarks
        elif q == 3 and pdgid not in {2112, 2212}:
            if _digit(pdgid, Location.N8) > 0:
                return True
            else:
                return False

    if _extra_bits(pdgid) > 0:
        return False
    if _fundamental_id(pdgid) > 0:
        return False

    if is_dyon(pdgid):
        return False

    if is_Rhadron(pdgid):
        iz = 7
        for loc in range(6, 1, -1):
            if _digit(pdgid, loc) == 0:
                iz = loc
            elif loc == iz - 1:
                # ignore squark or gluino
                pass
            else:
                if _digit(pdgid, loc) == q:
                    return True
        return False

    if (
        _digit(pdgid, Location.Nq3) == q
        or _digit(pdgid, Location.Nq2) == q
        or _digit(pdgid, Location.Nq1) == q
    ):
        return True

    if is_pentaquark(pdgid):
        if _digit(pdgid, Location.Nl) == q or _digit(pdgid, Location.Nr) == q:
            return True

    return False
