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

    A = property(_functions.A, doc=_functions.A.__doc__)
    J = property(_functions.J, doc=_functions.J.__doc__)
    L = property(_functions.L, doc=_functions.L.__doc__)
    S = property(_functions.S, doc=_functions.S.__doc__)
    Z = property(_functions.Z, doc=_functions.Z.__doc__)
    abspid = property(_functions.abspid, doc=_functions.abspid.__doc__)
    charge = property(_functions.charge, doc=_functions.charge.__doc__)
    has_bottom = property(_functions.has_bottom, doc=_functions.has_bottom.__doc__)
    has_charm = property(_functions.has_charm, doc=_functions.has_charm.__doc__)
    has_down = property(_functions.has_down, doc=_functions.has_down.__doc__)
    has_fundamental_anti = property(
        _functions.has_fundamental_anti, doc=_functions.has_fundamental_anti.__doc__
    )
    has_strange = property(_functions.has_strange, doc=_functions.has_strange.__doc__)
    has_top = property(_functions.has_top, doc=_functions.has_top.__doc__)
    has_up = property(_functions.has_up, doc=_functions.has_up.__doc__)
    is_Qball = property(_functions.is_Qball, doc=_functions.is_Qball.__doc__)
    is_Rhadron = property(_functions.is_Rhadron, doc=_functions.is_Rhadron.__doc__)
    is_SUSY = property(_functions.is_SUSY, doc=_functions.is_SUSY.__doc__)
    is_baryon = property(_functions.is_baryon, doc=_functions.is_baryon.__doc__)
    is_composite_quark_or_lepton = property(
        _functions.is_composite_quark_or_lepton,
        doc=_functions.is_composite_quark_or_lepton.__doc__,
    )
    is_diquark = property(_functions.is_diquark, doc=_functions.is_diquark.__doc__)
    is_dyon = property(_functions.is_dyon, doc=_functions.is_dyon.__doc__)
    is_gauge_boson_or_higgs = property(
        _functions.is_gauge_boson_or_higgs,
        doc=_functions.is_gauge_boson_or_higgs.__doc__,
    )
    is_generator_specific = property(
        _functions.is_generator_specific, doc=_functions.is_generator_specific.__doc__
    )
    is_hadron = property(_functions.is_hadron, doc=_functions.is_hadron.__doc__)
    is_lepton = property(_functions.is_lepton, doc=_functions.is_lepton.__doc__)
    is_meson = property(_functions.is_meson, doc=_functions.is_meson.__doc__)
    is_nucleus = property(_functions.is_nucleus, doc=_functions.is_nucleus.__doc__)
    is_pentaquark = property(
        _functions.is_pentaquark, doc=_functions.is_pentaquark.__doc__
    )
    is_quark = property(_functions.is_quark, doc=_functions.is_quark.__doc__)
    is_sm_gauge_boson_or_higgs = property(
        _functions.is_sm_gauge_boson_or_higgs,
        doc=_functions.is_sm_gauge_boson_or_higgs.__doc__,
    )
    is_special_particle = property(
        _functions.is_special_particle, doc=_functions.is_special_particle.__doc__
    )
    is_technicolor = property(
        _functions.is_technicolor, doc=_functions.is_technicolor.__doc__
    )
    is_valid = property(_functions.is_valid, doc=_functions.is_valid.__doc__)
    j_spin = property(_functions.j_spin, doc=_functions.j_spin.__doc__)
    l_spin = property(_functions.l_spin, doc=_functions.l_spin.__doc__)
    s_spin = property(_functions.s_spin, doc=_functions.s_spin.__doc__)
    three_charge = property(
        _functions.three_charge, doc=_functions.three_charge.__doc__
    )


# Verify the PDGID class has all relevant functions defined in the pdgid.functions module
for _n in _fnames:
    assert _n in dir(
        PDGID
    ), "{} missing from PDGID class! Update the list in pdgid.py".format(_n)
