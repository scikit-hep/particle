# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
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

HepPDT and HepPID versions 3.04.01: http://lcgapp.cern.ch/project/simu/HepPDT/
"""

from __future__ import print_function, division, absolute_import

# Backport needed if Python 2 is used
from enum import IntEnum


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
    """Is it a valid PDG ID?"""
    if _fundamental_id(pdgid) > 0: return True
    if is_meson(pdgid): return True
    if is_baryon(pdgid): return True
    if is_pentaquark(pdgid): return True
    if is_SUSY(pdgid): return True
    if is_Rhadron(pdgid): return True
    if is_dyon(pdgid): return True
    if is_diquark(pdgid): return True
    if is_pentaquark(pdgid): return True
    if _extra_bits(pdgid) > 0 :
        if is_nucleus(pdgid): return True
        if is_Qball(pdgid): return True
        return False
    return False


def abspid(pdgid):
    """Returns the absolute value of the PDG ID."""
    return abs(pdgid)


def is_lepton(pdgid):
    """Does this PDG ID correspond to a lepton?"""
    if _extra_bits(pdgid) > 0: return False
    if _fundamental_id(pdgid) >= 11 and _fundamental_id(pdgid) <= 18 : return True
    return False


def is_hadron(pdgid):
    """Does this PDG ID correspond to a hadron?"""
    if _extra_bits(pdgid) > 0 : return False
    if is_meson(pdgid): return True
    if is_baryon(pdgid): return True
    if is_pentaquark(pdgid): return True
    return False


def is_meson(pdgid):
    """Does this PDG ID correspond to a meson?"""
    if _extra_bits(pdgid) > 0 : return False
    if abspid(pdgid) <= 100 : return False
    if _fundamental_id(pdgid) <= 100 and _fundamental_id(pdgid) > 0 : return False
    if abspid(pdgid) in (130, 210, 310) : return True
    if abspid(pdgid) in (150, 350, 510, 530) : return True
    if pdgid in (110, 990, 9990) : return True
    if (_digit(pdgid, Location.Nj) > 0
        and _digit(pdgid, Location.Nq3) > 0
        and _digit(pdgid, Location.Nq2) > 0
        and _digit(pdgid, Location.Nq1) == 0
        ):
        # check for illegal antiparticles
        if _digit(pdgid, Location.Nq3) == _digit(pdgid, Location.Nq2) and pdgid < 0 :
            return False
        else:
            return True
    return False


def is_baryon(pdgid):
    """Does this PDG ID correspond to a baryon?"""
    if abspid(pdgid) <= 100 : return False
    if _extra_bits(pdgid) > 0: return False
    if _fundamental_id(pdgid) > 0 and _fundamental_id(pdgid) <= 100 : return False
    if abspid(pdgid) == 2110 or abspid(pdgid) == 2210 : return True
    if _digit(pdgid, Location.Nj) > 0 and _digit(pdgid, Location.Nq3) > 0 and _digit(pdgid, Location.Nq2) > 0 and _digit(pdgid, Location.Nq1) > 0 : return True
    if is_Rhadron(pdgid) or is_pentaquark(pdgid) : return False
    return False


def is_diquark(pdgid):
    """Does this PDG ID correspond to a diquark?"""
    if _extra_bits(pdgid) > 0 : return False
    if abspid(pdgid) <= 100 : return False
    if _fundamental_id(pdgid) <= 100 and _fundamental_id(pdgid) > 0 : return False
    if _digit(pdgid, Location.Nj) > 0 and _digit(pdgid, Location.Nq3) == 0 and _digit(pdgid, Location.Nq2) > 0 and _digit(pdgid, Location.Nq1) > 0 : return True
    return False


def is_nucleus(pdgid):
    """
    Does this PDG ID correspond to a nucleus?

    Ion numbers are +/- 10LZZZAAAI.
    AAA is A - total baryon number
    ZZZ is Z - total charge
    L is the total number of strange quarks.
    I is the isomer number, with I=0 corresponding to the ground state.
    """
    # A proton can also be a Hydrogen nucleus
    if abspid(pdgid) == 2212 :  return True
    if _digit(pdgid, Location.N10) == 1 and _digit(pdgid, Location.N9) == 0 :
        # Charge should always be less than or equal to the baryon number
        if A(pdgid) >= Z(pdgid) : return True
    return False


def is_pentaquark(pdgid):
    """
    Does the PDG ID correspond to a pentaquark?

    Pentaquark IDs are of the form +/- 9 Nr Nl Nq1 Nq2 Nq3 Nj, where Nj = 2J + 1 gives the spin
    and Nr Nl Nq1 Nq2 Nq3 denote the quark numbers in order Nr >= Nl >= Nq1 >= Nq2
    and Nq3 gives the antiquark number.
    """
    if _extra_bits(pdgid) > 0 : return False
    if _digit(pdgid, Location.N) != 9: return False
    if _digit(pdgid, Location.Nr) == 9 or _digit(pdgid, Location.Nr) == 0 : return False
    if _digit(pdgid, Location.Nj) == 9 or _digit(pdgid, Location.Nl) == 0 : return False
    if _digit(pdgid, Location.Nq1) == 0 : return False
    if _digit(pdgid, Location.Nq2) == 0 : return False
    if _digit(pdgid, Location.Nq3) == 0 : return False
    if _digit(pdgid, Location.Nj) == 0 : return False
    if _digit(pdgid, Location.Nq2) > _digit(pdgid, Location.Nq1) : return False
    if _digit(pdgid, Location.Nq1) > _digit(pdgid, Location.Nl) : return False
    if _digit(pdgid, Location.Nl) > _digit(pdgid, Location.Nr) : return False
    return True


def is_Rhadron(pdgid):
    """Does this PDG ID correspond to an R-hadron?

    An R-hadron is of the form 10abcdj, 100abcj, or 1000abj,
    where j = 2J + 1 gives the spin; b, c, and d are quarks or gluons;
    and a (the digit following the zero's) is a SUSY particle.
    """
    if _extra_bits(pdgid) > 0 : return False
    if _digit(pdgid, Location.N) != 1 : return False
    if _digit(pdgid, Location.Nr) != 0 : return False
    if is_SUSY(pdgid): return False
    # All R-hadrons have at least 3 core digits
    if _digit(pdgid, Location.Nq2) == 0 or _digit(pdgid, Location.Nq3) == 0 or _digit(pdgid, Location.Nj) == 0 : return False
    return True


def is_Qball(pdgid):
    """
    Does this PDG ID correspond to a Q-ball or any exotic particle with electric charge beyond the qqq scheme?

    Ad-hoc numbering for such particles is +/- 100XXXY0, where XXX.Y is the charge.
    """
    if _extra_bits(pdgid) != 1 : return False
    if _digit(pdgid, Location.N) != 0 : return False
    if _digit(pdgid, Location.Nr) != 0 : return False
    if (abspid(pdgid)//10)%10000 == 0 : return False
    if _digit(pdgid, Location.Nj) != 0 : return False
    return True


def is_dyon(pdgid):
    """
    Does this PDG ID correspond to a Dyon, a magnetic monopole?

    Magnetic monopoles and Dyons are assumed to have one unit of Dirac monopole charge
    and a variable integer number xyz units of electric charge,
    where xyz stands for Nq1 Nq2 Nq3.

    Codes 411xyz0 are used when the magnetic and electrical charge sign agree and 412xyz0 when they disagree,
    with the overall sign of the particle set by the magnetic charge.
    For now, no spin information is provided.
    """
    if _extra_bits(pdgid) > 0 : return False
    if _digit(pdgid, Location.N) != 4 : return False
    if _digit(pdgid, Location.Nr) != 1 : return False
    if _digit(pdgid, Location.Nl) != 1 and _digit(pdgid, Location.Nl) != 2 : return False
    if _digit(pdgid, Location.Nq3) == 0 : return False
    if _digit(pdgid, Location.Nj) != 0 : return False
    return True


def is_SUSY(pdgid):
    """
    Does this PDG ID correspond to a SUSY particle?

    Fundamental SUSY particles have N = 1 or 2.
    """
    if _extra_bits(pdgid) > 0 : return False
    if _digit(pdgid, Location.N) != 1 and _digit(pdgid, Location.N) != 2 : return False
    if _digit(pdgid, Location.Nr) != 0 : return False
    if _fundamental_id(pdgid) == 0 : return False
    return True


def has_down(pdgid):
    """Does this particle contain a down quark?"""
    return _has_quark_q(pdgid, 1)


def has_up(pdgid):
    """Does this particle contain an up quark?"""
    return _has_quark_q(pdgid, 2)


def has_strange(pdgid):
    """Does this particle contain a strange quark?"""
    return _has_quark_q(pdgid, 3)


def has_charm(pdgid):
    """Does this particle contain a charm quark?"""
    return _has_quark_q(pdgid, 4)


def has_bottom(pdgid):
    """Does this particle contain a bottom quark?"""
    return _has_quark_q(pdgid, 5)


def has_top(pdgid):
    """Does this particle contain a top quark?"""
    return _has_quark_q(pdgid, 6)


def has_fundamental_anti(pdgid):
    """If this is a fundamental particle, does it have a valid antiparticle?"""
    # These are defined by the generator and therefore are always valid
    fid = _fundamental_id(pdgid)
    if fid in range(80, 101): return True
    # Check PDGIDs from 1 to 79
    _cp_conjugates = (21, 22, 23, 25, 32, 33, 35, 36, 39, 41)
    if fid in range(1, 80) and fid not in _cp_conjugates and is_valid(abs(pdgid)) : return True
    return False


def charge(pdgid):
    """Returns the charge."""
    if not is_valid(pdgid): return None
    if not is_Qball(pdgid):
        return three_charge(pdgid)/3.
    else:
        return three_charge(pdgid)/30.


def three_charge(pdgid):
    """
    Returns 3 times the charge.

    None is returned if the PDGID is not valid.
    """
    if not is_valid(pdgid): return None

    aid = abspid(pdgid)
    charge = None
    ch100 = [-1,  2, -1, 2, -1, 2, -1, 2, 0, 0,
             -3,  0, -3, 0, -3, 0, -3, 0, 0, 0,
              0,  0,  0, 3,  0, 0,  0, 0, 0, 0,
              0,  0,  0, 3,  0, 0,  3, 0, 0, 0,
              0, -1,  0, 0,  0, 0,  0, 0, 0, 0,
              0,  6,  3, 6,  0, 0,  0, 0, 0, 0,
              0,  0,  0, 0,  0, 0,  0, 0, 0, 0,
              0,  0,  0, 0,  0, 0,  0, 0, 0, 0,
              0,  0,  0, 0,  0, 0,  0, 0, 0, 0,
              0,  0,  0, 0,  0, 0,  0, 0, 0, 0
              ]
    q1 = _digit(pdgid, Location.Nq1)
    q2 = _digit(pdgid, Location.Nq2)
    q3 = _digit(pdgid, Location.Nq3)
    sid = _fundamental_id(pdgid)

    if _extra_bits(pdgid) > 0:
        if is_nucleus(pdgid):     # ion
            return 3*Z(pdgid)
        elif is_Qball(pdgid):     # Qball
            charge = 3*((aid//10)%10000)
        else:            # this should never be reached in the present numbering scheme
            return None  # since extra bits exist only for Q-balls and nuclei
    elif is_dyon(pdgid):            # Dyon
        charge = 3*( (aid//10)%1000 )
        # this is half right
        # the charge sign will be changed below if pid < 0
        if _digit(pdgid, Location.Nl) == 2:
            charge = -charge
    elif sid > 0 and sid <= 100:        # use table
        charge = ch100[sid-1]
        if aid in (1000017, 1000018, 1000034, 1000052, 1000053, 1000054) : charge = 0
        if aid == 5100061 or aid == 5100062 : charge = 6
    elif _digit(pdgid, Location.Nj) == 0 :      # KL, KS, or undefined
        return 0
    elif q1 == 0 or (is_Rhadron(pdgid) and q1 == 9 ): # mesons
        if q2 == 3 or q2 == 5 :
            charge = ch100[q3-1] - ch100[q2-1]
        else:
            charge = ch100[q2-1] - ch100[q3-1]
    elif q3 == 0:                       # diquarks
        charge = ch100[q2-1] + ch100[q1-1]
    elif is_baryon(pdgid) or (is_Rhadron(pdgid) and _digit(pdgid, Location.Nl) == 9) :  # baryons
        charge = ch100[q3-1] + ch100[q2-1] + ch100[q1-1]
    if charge == 0 : return 0
    elif pdgid < 0 : charge = -charge
    return charge


def j_spin(pdgid):
    """Returns the total spin as 2J+1."""
    if not is_valid(pdgid): return None
    if _fundamental_id(pdgid)>0:
        fund = _fundamental_id(pdgid)
        if fund > 0 and fund < 7 : return 2  # 4th generation quarks not dealt with !
        if fund == 9 : return 3
        if fund > 10 and fund < 17 : return 2  # 4th generation leptons not dealt with !
        if fund > 20 and fund < 25 : return 3
        return None
    elif _extra_bits(pdgid) > 0 : return None
    if pdgid in (130, 310): return 1   # Special cases of the KS and KL !
    return abspid(pdgid) % 10

def J(pdgid):
    """Returns the total spin J."""
    value = j_spin(pdgid)
    return (value - 1) / 2 if value is not None else value  # This works due to the Python 3 style division


def S(pdgid):
    """
    Returns the spin S.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    if not is_meson(pdgid): return None
    if not is_valid(pdgid): return None

    nl = (abspid(pdgid)//10000) % 10
    js = abspid(pdgid) % 10
    if (abspid(pdgid)//1000000)%10 == 9 : return None   # no knowledge so far
    if nl == 0 and js >= 3 : return 1
    elif nl == 0 and js == 1 : return 0
    elif nl == 1 and js >= 3 : return 0
    elif nl == 2 and js >= 3 : return 1
    elif nl == 1 and js == 1 : return 1
    elif nl == 3 and js >= 3 : return 1
    return 0


def s_spin(pdgid):
    """
    Returns the spin S as 2S+1.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    value = S(pdgid)
    return (2*value+1) if value is not None else value


def L(pdgid):
    """
    Returns the orbital angular momentum L.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    if not is_meson(pdgid): return None
    if not is_valid(pdgid): return None

    nl = (abspid(pdgid)//10000) % 10
    js = abspid(pdgid) % 10
    if (abspid(pdgid)//1000000)%10 == 9 : return None   # no knowledge so far

    if nl == 0 and js == 3: return 0
    elif nl == 0 and js == 5: return 1
    elif nl == 0 and js == 7: return 2
    elif nl == 0 and js == 9: return 3
    elif nl == 0 and js == 1: return 0
    elif nl == 1 and js == 3: return 1
    elif nl == 1 and js == 5: return 2
    elif nl == 1 and js == 7: return 3
    elif nl == 1 and js == 9: return 4
    elif nl == 2 and js == 3: return 1
    elif nl == 2 and js == 5: return 2
    elif nl == 2 and js == 7: return 3
    elif nl == 2 and js == 9: return 4
    elif nl == 1 and js == 1: return 1
    elif nl == 3 and js == 3: return 2
    elif nl == 3 and js == 5: return 3
    elif nl == 3 and js == 7: return 4
    elif nl == 3 and js == 9: return 5
    return 0


def l_spin(pdgid):
    """
    Returns the orbital angular momentum L as 2L+1.

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    value = L(pdgid)
    return (2*value+1) if value is not None else value


def P(pdgid):
    """
    Returns the parity quantum number P = (-1)^(L+1).

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    if not is_meson(pdgid): return None
    if not is_valid(pdgid): return None

    # At this stage it is guaranteed that L != None
    return (-1)**(L(pdgid)+1) if L(pdgid) is not None else None


def C(pdgid):
    """
    Returns the charge conjugation quantum number C = (-1)^(L+S).

    Notes
    -----
    - This is valid for mesons only. None is returned otherwise.
    - Mesons with PDGIDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
      and None is returned too.
    """
    if not is_meson(pdgid) or not three_charge(pdgid) == 0: return None
    if not is_valid(pdgid): return None

    if L(pdgid) is None or S(pdgid) is None:
        return None

    # At this stage it is guaranteed that L and S != None
    return (-1)**(L(pdgid)+S(pdgid))


def A(pdgid):
    """Returns the atomic number A if the PDG ID corresponds to a nucleus. Else it returns None."""
    # A proton can also be a Hydrogen nucleus
    if abspid(pdgid) == 2212 : return 1
    if _digit(pdgid, Location.N10) != 1 or _digit(pdgid, Location.N9) != 0 : return None
    return (abspid(pdgid)//10) % 1000


def Z(pdgid):
    """Returns the charge Z if the PDG ID corresponds to a nucleus. Else it returns None."""
    # A proton can also be a Hydrogen nucleus
    if abspid(pdgid) == 2212: return 1
    if _digit(pdgid, Location.N10) != 1 or _digit(pdgid, Location.N9) != 0 : return None
    return (abspid(pdgid)//10000) % 1000


def _digit(pdgid, loc):
    """
    Provides a convenient index into the PDGID number, whose format is in base 10.

    Returns the digit at position 'loc' given that the right-most digit is at position 1.
    """
    sid = str(abspid(pdgid))
    return int(sid[-loc]) if loc <= len(sid) else 0


def _extra_bits(pdgid):
    """
    Returns everything beyond the 7th digit, so anything outside the PDG numbering scheme.
    """
    return abspid(pdgid) // 10000000


def _fundamental_id(pdgid):
    """
    Returns the first 2 digits if this is a "fundamental" particle.
    Returns 0 if the particle is not fundamental or not standard (PDG ID with more than 7 digits).

    PDGID=100 is a special case (internal generator ID's are 81-100).
    """
    if _extra_bits(pdgid) > 0 : return 0
    if _digit(pdgid, Location.Nq2) == 0 and _digit(pdgid, Location.Nq1) == 0 : return abspid(pdgid) % 10000
    elif abspid(pdgid) <= 100 : return abspid(pdgid)
    else: return 0


def _has_quark_q(pdgid, q):
    """Helper function - does this particle contain a quark q?"""
    if _extra_bits(pdgid) > 0 : return False
    if _fundamental_id(pdgid) > 0 : return False
    if is_dyon(pdgid): return False
    if is_Rhadron(pdgid):
        iz = 7
        for loc in range(6, 1, -1):
            if _digit(pdgid, loc) == 0 :
                iz = loc
            elif loc == iz-1 :
                #ignore squark or gluino
                pass
            else:
                if _digit(pdgid, loc) == q : return True
        return False
    if _digit(pdgid, Location.Nq3) == q or _digit(pdgid, Location.Nq2) == q or _digit(pdgid, Location.Nq1) == q: return True
    if is_pentaquark(pdgid):
        if _digit(pdgid, Location.Nl) == q or _digit(pdgid, Location.Nr) == q : return True
    return False
