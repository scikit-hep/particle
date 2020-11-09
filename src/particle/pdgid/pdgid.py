# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
Class representing a PDG ID.

All methods of HepPID are implemented in a Pythonic version, see the functions module.
"""

from __future__ import absolute_import

from . import functions as _functions

from inspect import isfunction


# Collect all the user defined, non-hidden functions in the pdgid.functions module
_fnames = [
    fname
    for fname in dir(_functions)
    if not fname.startswith("_") and isfunction(getattr(_functions, fname))
]


class PDGID(int):
    """
    Holds a PDG ID.

    Example
    -------
    >>> PDGID(11).is_lepton
    True
    """

    __slots__ = ()  # Keep PDGID a slots based class

    def __repr__(self):
        # type: () -> str
        return "<PDGID: {:d}{:s}>".format(
            int(self), "" if _functions.is_valid(self) else " (is_valid==False)"
        )

    def __str__(self):
        # type: () -> str
        return repr(self)

    def __neg__(self):
        # type: () -> PDGID
        return self.__class__(-int(self))

    __invert__ = __neg__

    def info(self):
        # type: () -> str
        """
        Print all PDGID properties one per line, for easy inspection.
        """
        val = ""
        for item in _fnames:
            val += "{item:14} {value}\n".format(item=item, value=getattr(self, item))
        return val

    A = property(_functions.A)
    J = property(_functions.J)
    L = property(_functions.L)
    S = property(_functions.S)
    Z = property(_functions.Z)
    abspid = property(_functions.abspid)
    charge = property(_functions.charge)
    has_bottom = property(_functions.has_bottom)
    has_charm = property(_functions.has_charm)
    has_down = property(_functions.has_down)
    has_fundamental_anti = property(_functions.has_fundamental_anti)
    has_strange = property(_functions.has_strange)
    has_top = property(_functions.has_top)
    has_up = property(_functions.has_up)
    is_Qball = property(_functions.is_Qball)
    is_Rhadron = property(_functions.is_Rhadron)
    is_SUSY = property(_functions.is_SUSY)
    is_baryon = property(_functions.is_baryon)
    is_composite_quark_or_lepton = property(_functions.is_composite_quark_or_lepton)
    is_diquark = property(_functions.is_diquark)
    is_dyon = property(_functions.is_dyon)
    is_gauge_boson_or_higgs = property(_functions.is_gauge_boson_or_higgs)
    is_generator_specific = property(_functions.is_generator_specific)
    is_hadron = property(_functions.is_hadron)
    is_lepton = property(_functions.is_lepton)
    is_meson = property(_functions.is_meson)
    is_nucleus = property(_functions.is_nucleus)
    is_pentaquark = property(_functions.is_pentaquark)
    is_quark = property(_functions.is_quark)
    is_sm_gauge_boson_or_higgs = property(_functions.is_sm_gauge_boson_or_higgs)
    is_special_particle = property(_functions.is_special_particle)
    is_technicolor = property(_functions.is_technicolor)
    is_valid = property(_functions.is_valid)
    j_spin = property(_functions.j_spin)
    l_spin = property(_functions.l_spin)
    s_spin = property(_functions.s_spin)
    three_charge = property(_functions.three_charge)


# Verify the PDGID class has all relevant functions defined in the pdgid.functions module
for _n in _fnames:
    assert _n in dir(
        PDGID
    ), "{} missing from PDGID class! Update the list in pdgid.py".format(_n)
