# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import, division, print_function

# Python standard library
import csv
from copy import copy

from functools import total_ordering

# External dependencies
import attr

from typing import (
    Optional,
    Any,
    Dict,
    Tuple,
    List,
    Callable,
    Iterable,
    SupportsInt,
    Union,
    TextIO,
    Set,
)

from hepunits.constants import c_light

from .. import data
from ..pdgid import PDGID
from ..pdgid import is_valid
from ..pdgid.functions import _digit
from ..pdgid.functions import Location
from .regex import getname, getdec
from .enums import (
    SpinType,
    Parity,
    Charge,
    Inv,
    Status,
    Parity_undo,
    Parity_prog,
    Charge_undo,
    Charge_prog,
    Charge_mapping,
)
from .utilities import programmatic_name, str_with_unc, latex_to_html_name
from .kinematics import width_to_lifetime
from ..converters.evtgen import EvtGenName2PDGIDBiMap


class ParticleNotFound(RuntimeError):
    pass


class InvalidParticle(RuntimeError):
    pass


def _isospin_converter(isospin):
    # type: (str) -> Optional[float]
    vals = {
        "0": 0.0,
        "1/2": 0.5,
        "1": 1.0,
        "3/2": 1.5,
    }  # type: Dict[Optional[str], Optional[float]]
    return vals.get(isospin, None)


def _none_or_positive_converter(value):
    # type: (float) -> Optional[float]
    return None if value < 0 else value


# These are needed to trick attrs typing
minus_one = -1.0  # type: Optional[float]
none_float = None  # type: Optional[float]


@total_ordering
@attr.s(slots=True, eq=False, order=False, repr=False)
class Particle(object):
    """
    The Particle object class. Hold a series of properties for a particle.

    Class properties:

    C
        The charge conjugation parity quantum number, if relevant.
        It is C = (-1)^(L+S) for self-conjugate mesons.
        Mesons with PDG IDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
        and None is returned.

    G
        The G-parity quantum number, if relevant.

    I
        The isospin quantum number, if relevant.

    P
        The parity quantum number, if relevant.
        It is P = (-1)^(L+1) for self-conjugate mesons and -1 for the photon.
        Mesons with PDG IDs of the kind 9XXXXXX (N=9) are not experimentally well-known particles
        and None is returned.

    anti_flag
        The particle-antiparticle flag.

        A = B     - particle that has anti-particle partner different from particle
                    with ASCII name formed by concatenation of the name shown below with charge
                    ( e- <--> e+, pi+ <--> pi-, K+ <--> K-, W+ <--> W- ).
        A = F     - particle that has anti-particle partner different from particle
                    with ascii name formed by concatenation of the name shown below with string "bar" and charge
                    by the rule (nu(e) <--> nubar(e), p <--> pbar, Delta++ <--> Deltabar--)
        A = blank - particle that coincides with its antiparticle (gamma, pi0, eta).

    charge
        The particle charge, in units of the positron charge.

    latex_name
        The particle name in LaTeX.

    mass
        The particle mass, in MeV.

    mass_lower
        The lower uncertainty on the particle mass, in MeV.

    mass_upper
        The upper uncertainty on the particle mass, in MeV.

    pdgid
        The PDG ID.

    pdg_name
        The particle name as in the PDG data file.

        Note:
        This name does not contain the charge. See alternative `name`.

    quarks
        The quark content of the particle. Empty string if not relevant.

        Note:
        Capital letters represent anti-quarks, 'qQ' stands for light quark,
        light anti-quark pair with unknown wave functions.
        x, y stand for wave function coefficients, see the Review of Particle Physics (RPP) 'Quark Model' Review.
        p, q stand for CP violation parameters, see the RPP 'CP violation in KL Decays' review.

    rank
        The particle rank as specified by the PDG, i.e. the number of baryon stars - used only on baryons.

        Possible values are:
        4 - Existence is certain, and properties are at least fairly well explored.
        3 - Existence ranges from very likely to certain, but further confirmation
             is desirable and/or quantum numbers, branching fractions, etc. are not well determined.
        2 - Evidence of existence is only fair.
        1 - Evidence of existence is poor.

    status
        The particle status as specified by the PDG.

        Possible values are:
        R - Established particles in the Review of Particle Physics (RPP) Summary Table
            in Particle Physics Booklet
            (established quarks, gauge bosons, leptons, mesons and baryons, except those in D below).
        D - The particle is omitted from the Summary Tables in the Particle Physics Booklet,
            but not from the Review. These entries are omitted only to save space
            even though they are well established.
        S - The particle is omitted from the particle properties Summary Tables
            because it is not well established.
        F - Special case: "Further mesons", see RPP, these states are in the RPP database
            but are poorly established or observed by a single group and thus need confirmation.
            If used, these should be referred to the original publication.

    width
        The particle decay width, in MeV.

    width_lower
        The lower uncertainty on the particle decay width, in MeV.

    width_upper
        The upper uncertainty on the particle decay width, in MeV.
    """

    pdgid = attr.ib(converter=PDGID)
    pdg_name = attr.ib()
    mass = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )  # type: Optional[float]
    mass_upper = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )  # type: Optional[float]
    mass_lower = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )  # type: Optional[float]
    width = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )  # type: Optional[float]
    width_upper = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )  # type: Optional[float]
    width_lower = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )  # type: Optional[float]
    _three_charge = attr.ib(Charge.u, converter=Charge)  # charge * 3
    I = attr.ib(none_float, converter=_isospin_converter)  # type: Optional[float]
    # J = attr.ib(None)  # Total angular momentum
    G = attr.ib(Parity.u, converter=Parity)  # Parity: '', +, -, or ?
    P = attr.ib(Parity.u, converter=Parity)  # Space parity
    C = attr.ib(Parity.u, converter=Parity)  # Charge conjugation parity
    anti_flag = attr.ib(
        Inv.Same, converter=Inv
    )  # Info about particle name for anti-particles
    rank = attr.ib(0)
    status = attr.ib(Status.NotInPDT, converter=Status)
    quarks = attr.ib("", converter=str)
    latex_name = attr.ib("Unknown")

    def __repr__(self):
        # type: () -> str
        return '<{self.__class__.__name__}: name="{self!s}", pdgid={pdgid}, mass={mass}>'.format(
            self=self, pdgid=int(self.pdgid), mass=self._str_mass()
        )

    # Loaded table of entries
    _table = None  # type: Optional[Set[Particle]]

    # Names of loaded tables
    _table_names = None  # type: Optional[List[str]]

    @classmethod
    def table_names(cls):
        # type: () -> Tuple[str, ...]
        """
        Return the list of names loaded.

        Note
        ----
        Calling this class method will load the default table,
        if no table has so far been loaded.
        Check with table_loaded() first if you don't want this loading
        to be triggered by the call.
        """

        if cls._table_names is None:
            cls.load_table()

        if cls._table_names is not None:
            return tuple(cls._table_names)  # make a copy to avoid user manipulation
        else:
            return tuple()

    @classmethod
    def table_loaded(cls):
        # type: () -> bool
        """
        Check to see if the table is loaded.
        """
        return not cls._table is None

    @classmethod
    def all(cls):
        # type: () -> Set[Particle]
        """
        Access, hence get hold of, the internal particle data CSV table,
        loading it from the default location if no table has yet been loaded.
        All `Particle` (instances) are returned as a list.
        """
        if not cls.table_loaded():
            cls.load_table()

        return cls._table if cls._table is not None else set()

    @classmethod
    def dump_table(
        cls,
        exclusive_fields=(),  # type: Iterable[str]
        exclude_fields=(),  # type: Iterable[str]
        n_rows=-1,
        filter_fn=None,  # type: Optional[Callable[[Particle], bool]]
        filename=None,  # type: Optional[str]
        tablefmt="simple",
        floatfmt=".12g",
        numalign="decimal",
    ):
        # type: (...) -> Optional[str]
        """
        Dump the internal particle data CSV table,
        loading it from the default location if no table has yet been loaded.

        The table attributes are those of the class. By default all attributes
        are used as table fields. Their complete list is:
            pdgid
            pdg_name
            mass
            mass_upper
            mass_lower
            width
            width_upper
            width_lower
            three_charge
            I
            G
            P
            C
            anti_flag
            rank
            status
            quarks
            latex_name

        Optionally dump to a file.

        Parameters
        ----------
        exclusive_fields: list, optional, default is []
            Exclusive list of fields to print out.
        exclude_fields: list, optional, default is []
            List of table fields to exclude in the printout.
            Relevant only when exclusive_fields is not given.
        n_rows: int, optional, defaults to all rows
            Number of table rows to print out.
        filter_fn: function, optional, default is None
            Apply a filter to each particle.
            See findall(...) for typical use cases.
        filename: str, optional, default is None
            Name of file where to dump the table.
            By default the table is dumped to stdout.
        tablefmt: str, optional, default is 'simple'
            Table formatting option, see the tabulate's package
            tabulate function for a description of available options.
            The most common options are:
            'plain', 'simple', 'grid', 'rst', 'html', 'latex'.
        floatfmt: str, optional, default is '.12g'
            Number formatting, see the tabulate's package
            tabulate function for a description of available options.
        numalign: str or None, oprional, default is 'decimal'
            Column alignment for numbers, see the tabulate's package
            tabulate function for a description of available options.

        Returns
        -------
        str or None if filename is None or not, respectively.

        Note
        ----
        Uses the `tabulate` package.

        Examples
        --------
        print(Particle.dump_table())
        print(Particle.dump_table(n_rows=5))
        print(Particle.dump_table(exclusive_fields=['pdgid', 'pdg_name']))
        print(Particle.dump_table(filter_fn=lambda p: p.pdgid.has_bottom))
        Particle.dump_table(filename='output.txt', tablefmt='rst')
        """
        from tabulate import tabulate

        if not cls.table_loaded():
            cls.load_table()

        # Get all table headers from the class attributes
        tbl_names = [a.name for a in Particle.__attrs_attrs__]  # type: ignore
        # ... and replace '_three_charge' with the better, public property
        tbl_names[tbl_names.index("_three_charge")] = "three_charge"

        if exclusive_fields:
            tbl_names = list(exclusive_fields)
        else:
            for fld in exclude_fields:
                try:
                    tbl_names.remove(fld)
                except:
                    pass

        # Start with the full table
        tbl_all = sorted(cls.all())

        # Apply a filter, if specified
        if filter_fn is not None:
            tbl_all = cls.findall(filter_fn)

        # In any case, only dump a given number of rows?
        if n_rows >= 0:
            tbl_all = tbl_all[:n_rows]

        # Build all table rows
        tbl = []
        for p in tbl_all:
            tbl.append([getattr(p, attr) for attr in tbl_names])

        if filename:
            filename = str(filename)  # Conversion to handle pathlib on Python < 3.6
            with open(filename, "w") as outfile:
                print(
                    tabulate(
                        tbl,
                        headers=tbl_names,
                        tablefmt=tablefmt,
                        floatfmt=floatfmt,
                        numalign=numalign,
                    ),
                    file=outfile,
                )
            return None
        else:
            return tabulate(
                tbl,
                headers=tbl_names,
                tablefmt=tablefmt,
                floatfmt=floatfmt,
                numalign=numalign,
            )

    @classmethod
    def load_table(cls, filename=None, append=False, _name=None):
        # type: (Union[None, str, TextIO], bool, Optional[str]) -> None
        """
        Load a particle data CSV table. Optionally append to the existing data already loaded if append=True.
        As a special case, if this is called with append=True and the table is not loaded, the default will
        be loaded first before appending (set append=False if you don't want this behavior).

        A parameter is also included that should be considered private for now. It is _name, which
        will override the filename for the stored filename in _table_names.
        """

        if append and not cls.table_loaded():
            cls.load_table(append=False)  # default load
        elif not append:
            cls._table = set()
            cls._table_names = []

        # Tell MyPy that this is true
        assert cls._table is not None
        assert cls._table_names is not None

        if filename is None:
            with data.open_text(data, "particle2019.csv") as f:
                cls.load_table(f, append=append, _name="particle2019.csv")
            with data.open_text(data, "nuclei2020.csv") as f:
                cls.load_table(f, append=True, _name="nuclei2020.csv")
            return
        elif not hasattr(filename, "read"):
            cls._table_names.append(str(filename))
            # Conversion to handle pathlib on Python < 3.6:
            open_file = open(str(filename))
        else:
            assert not isinstance(filename, str)  # Tell typing that this is true
            tmp_name = _name or getattr(filename, "name")
            cls._table_names.append(
                tmp_name or "{0!r} {1}".format(filename, len(cls._table_names))
            )
            open_file = filename

        with open_file as f:
            r = csv.DictReader(l for l in f if not l.startswith("#"))

            for v in r:
                try:
                    value = int(v["ID"])

                    # Replace the previous value if it exists
                    # We can remove an int; ignore typing thinking we need a particle
                    if value in cls._table:
                        cls._table.remove(value)  # type: ignore

                    cls._table.add(
                        cls(
                            pdgid=value,
                            mass=float(v["Mass"]),
                            mass_upper=float(v["MassUpper"]),
                            mass_lower=float(v["MassLower"]),
                            width=float(v["Width"]),
                            width_upper=float(v["WidthUpper"]),
                            width_lower=float(v["WidthLower"]),
                            I=v["I"],
                            G=int(v["G"]),
                            P=int(v["P"]),
                            C=int(v["C"]),
                            anti_flag=int(v["Anti"]),
                            three_charge=int(v["Charge"]),
                            rank=int(v["Rank"]),
                            status=int(v["Status"]),
                            pdg_name=v["Name"],
                            quarks=v["Quarks"],
                            latex_name=v["Latex"],
                        )
                    )
                except ValueError:
                    pass

    # The following __le__ and __eq__ needed for total ordering (sort, etc)

    def __le__(self, other):
        # type: (Any) -> bool
        # Sort by absolute particle numbers
        # The positive one should come first
        if type(self) == type(other):
            return abs(int(self) - 0.25) < abs(int(other) - 0.25)

        # Comparison with anything else should produce normal comparisons.
        else:
            return int(self) < other

    def __eq__(self, other):
        # type: (Any) -> bool
        try:
            return self.pdgid == other.pdgid
        except AttributeError:
            return self.pdgid == other

    # Only one particle can exist per PDGID number
    def __hash__(self):
        # type: () -> int
        return hash(self.pdgid)

    # Integer == PDGID
    def __int__(self):
        # type: () -> int
        return int(self.pdgid)

    # Shared with PDGID

    @property
    def J(self):
        # type: () -> int
        """
        The total spin J quantum number.

        Note that the returned value corresponds to that effectively encoded
        in the particle PDG ID.
        """
        return self.pdgid.J  # type: ignore

    @property
    def L(self):
        # type: () -> Optional[int]
        """
        The orbital angular momentum L quantum number (None if not a meson).

        Note that the returned value corresponds to that effectively encoded
        in the particle PDG ID.
        """
        return self.pdgid.L  # type: ignore

    @property
    def S(self):
        # type: () -> Optional[int]
        """
        The spin S quantum number (None if not a meson).

        Note that the returned value corresponds to that effectively encoded
        in the particle PDG ID.
        """
        return self.pdgid.S  # type: ignore

    @property
    def charge(self):
        # type: () -> Optional[float]
        """
        The particle charge, in units of the positron charge.

        Design note: the particle charge can also be retrieved from the particle PDG ID.
        To allow for user-defined particles, it is necessary to rather store
        the particle charge in the data tables themselves.
        Consistency of both ways of retrieving the particle charge is guaranteed
        for all PDG table particles.
        """
        return self.three_charge / 3 if self.three_charge is not None else None  # type: ignore

    @property
    def three_charge(self):
        # type: () -> Optional[int]
        "Three times the particle charge (charge * 3), in units of the positron charge."
        if not self.pdgid.is_nucleus:  # type: ignore
            # Return int(...) not to return the actual enum Charge
            return int(self._three_charge) if self._three_charge != Charge.u else None
        else:
            return self.pdgid.three_charge  # type: ignore

    @property
    def lifetime(self):
        # type: () -> Optional[float]
        """
        The particle lifetime, in nanoseconds.

        None is returned if the particle width (stored in the DB) is unknown.
        """
        return width_to_lifetime(self.width) if self.width is not None else None

    @property
    def ctau(self):
        # type: () -> Optional[float]
        """
        The particle c*tau, in millimeters.

        None is returned if the particle width (stored in the DB) is unknown.
        """
        return (
            c_light * self.lifetime
            if self.width is not None and self.lifetime is not None
            else None
        )

    @property
    def is_name_barred(self):
        # type: () -> bool
        """
        Check to see if particle is inverted (hence is it an antiparticle)
        and has a bar in its name.
        """
        return self.pdgid < 0 and self.anti_flag == Inv.Barred

    @property
    def spin_type(self):
        # type: () -> SpinType
        """
        Access the SpinType enum.

        Note that this is relevant for bosons only. SpinType.NonDefined is returned otherwise.
        """
        # Non-valid or non-standard PDG IDs
        if self.pdgid.j_spin is None:  # type: ignore
            return SpinType.NonDefined

        # Fermions - 2J+1 is always an even number
        if self.pdgid.j_spin % 2 == 0:  # type: ignore
            return SpinType.NonDefined

        if self.J in [0, 1, 2]:
            J = int(self.J)

            if self.P == Parity.p:
                return (SpinType.Scalar, SpinType.Axial, SpinType.Tensor)[J]
            elif self.P == Parity.m:
                return (SpinType.PseudoScalar, SpinType.Vector, SpinType.PseudoTensor)[
                    J
                ]

        return SpinType.Unknown

    @property
    def is_self_conjugate(self):
        # type: () -> bool
        """
        Is the particle self-conjugate, i.e. its own antiparticle?
        """
        return self.anti_flag == Inv.Same

    @property
    def is_unflavoured_meson(self):
        # type: () -> bool
        """
        Unflavoured mesons are self-conjugate (hence zero-charge) mesons
        with all their flavour (strange, charm, bottom and top) quantum numbers equal to zero.
        """
        if self.is_self_conjugate and self.three_charge == 0 and self.pdgid.is_meson:  # type: ignore
            return True
        else:
            return False

    def invert(self):
        # type: () -> Particle
        "Get the antiparticle."
        if self.anti_flag == Inv.Barred or (
            self.anti_flag == Inv.ChargeInv and self.three_charge != Charge.o
        ):
            return self.from_pdgid(-self.pdgid)
        else:
            return copy(self)

    __neg__ = invert
    __invert__ = invert

    # Pretty descriptions

    def __str__(self):
        # type: () -> str
        _tilde = "~" if self.anti_flag == Inv.Barred and self.pdgid < 0 else ""
        _charge = self._str_charge() if self._charge_in_name() else ""
        return self.pdg_name + _tilde + _charge

    name = property(
        __str__,
        doc="The nice name, with charge added, and a tilde for an antiparticle, if relevant.",
    )

    def _repr_latex_(self):
        # type: () -> str
        name = self.latex_name
        return ("$" + name + "$") if self.latex_name else "?"

    def _width_or_lifetime(self):
        # type: () -> str
        """
        Display either the particle width or the lifetime.
        Internally used by the describe() method.

        Note
        ----
        Width errors equal to None flag an experimental upper limit on the width.
        """
        if self.width is None:
            return "Width = None"
        elif self.width == 0:
            return "Width = 0.0 MeV"
        elif self.width_lower is None or self.width_upper is None:
            return "Width < {width} MeV".format(width=self.width)
        elif (
            self.width < 0.05
        ):  # corresponds to a lifetime of approximately 1.3e-20 seconds
            assert self.lifetime is not None
            if self.width_lower == self.width_upper:
                e = width_to_lifetime(self.width - self.width_lower) - self.lifetime
                s = "Lifetime = {lifetime} ns".format(
                    lifetime=str_with_unc(self.lifetime, e, e)
                )
            else:
                s = "Lifetime = {lifetime} ns".format(
                    lifetime=str_with_unc(
                        self.lifetime,
                        width_to_lifetime(self.width - self.width_lower)
                        - self.lifetime,
                        self.lifetime
                        - width_to_lifetime(self.width + self.width_upper),
                    )
                )
            return s
        else:
            return "Width = {width} MeV".format(
                width=str_with_unc(self.width, self.width_upper, self.width_lower)
            )

    def _charge_in_name(self):
        # type: () -> bool
        """Assess whether the particle charge is part of the particle name.

        Internally used when creating the name.
        """
        if self.anti_flag == Inv.ChargeInv:
            return True  # antiparticle flips sign of particle
        if self.pdgid in (23, 25, 111, 130, 310, 311, -311):
            return True  # the Z0, H0, pi0, KL0, KS0, K0 and K0bar
        if self.pdgid.is_diquark:  # type: ignore
            return False
        if abs(self.pdgid) in (2212, 2112):
            return False  # proton and neutron
        if abs(self.pdgid) < 19:
            return False  # all quarks and neutrinos (charged leptons dealt with in 1st line of if statements ;-))
        if self.three_charge is None:
            return False  # deal with corner cases ;-)
        if self.is_self_conjugate:
            pid = self.pdgid
            if pid < 25:
                return False  # Gauge bosons
            # Quarkonia never exhibit the 0 charge
            # All eta, eta', h, h', omega, phi, f, f' light mesons are supposed to have an s-sbar component (see PDG site),
            # but some particles have pdgid.has_strange==False :S! Play it safe ...
            elif any(
                [
                    chr in self.pdg_name
                    for chr in ("eta", "h(", "h'(", "omega", "phi", "f", "f'")
                ]
            ):
                return False
            elif pid.has_strange or pid.has_charm or pid.has_bottom or pid.has_top:  # type: ignore
                return False
            else:  # Light unflavoured mesons
                return True
        # Lambda baryons
        if (
            self.pdgid.is_baryon  # type: ignore
            and _digit(self.pdgid, Location.Nq2) == 1
            and self.I
            == 0.0  # 1st check alone is not sufficient to filter out lowest-ground Sigma's
            and self.pdgid.has_strange  # type: ignore
            and not (
                self.pdgid.has_charm or self.pdgid.has_bottom or self.pdgid.has_top  # type: ignore
            )
        ):
            return False
        if self.pdgid.is_nucleus:  # type: ignore
            return False
        return True

    def _str_charge(self):
        # type: () -> str
        """
        Display a reasonable particle charge printout.
        Internally used by the describe() and __str__ methods.
        """
        if self._three_charge is None:
            return "None"
        elif not self.pdgid.is_nucleus:  # type: ignore
            return Charge_undo[Charge(self._three_charge)]
        else:
            return str(self.pdgid.charge)  # type: ignore

    def _str_mass(self):
        # type: () -> str
        """
        Display a reasonable particle mass printout
        even when no mass value is available.
        Internally used by the describe() method.
        """
        if self.mass is None:
            return "None"
        else:
            return "{0} MeV".format(
                str_with_unc(self.mass, self.mass_upper, self.mass_lower)
            )

    def describe(self):
        # type: () -> str
        "Make a nice high-density string for a particle's properties."
        if self.pdgid == 0:
            return "Name: Unknown"

        val = """Name: {self!s:<14} ID: {self.pdgid:<12} Latex: {latex_name}
Mass  = {mass}
{width_or_lifetime}
Q (charge)        = {Q:<6}  J (total angular) = {self.J!s:<7}  P (space parity) = {P}
C (charge parity) = {C:<6}  I (isospin)       = {self.I!s:<7}  G (G-parity)     = {G}
""".format(
            self=self,
            G=Parity_undo[self.G],
            C=Parity_undo[self.C],
            Q=self._str_charge(),
            P=Parity_undo[self.P],
            mass=self._str_mass(),
            width_or_lifetime=self._width_or_lifetime(),
            latex_name=self._repr_latex_(),
        )

        if self.spin_type != SpinType.Unknown:
            val += "    SpinType: {self.spin_type!s}\n".format(self=self)
        if self.quarks:
            val += "    Quarks: {self.quarks}\n".format(self=self)
        val += "    Antiparticle name: {iself.name} (antiparticle status: {self.anti_flag.name})".format(
            iself=self.invert(), self=self
        )
        return val

    @property
    def evtgen_name(self):
        # type: () -> str
        "This is the name used in EvtGen."
        return EvtGenName2PDGIDBiMap[self.pdgid]

    @property
    def programmatic_name(self):
        # type: () -> str
        "This name could be used for a variable name."
        return programmatic_name(self.name)

    @property
    def html_name(self):
        # type: () -> str
        "This is the name using HTML instead of LaTeX."
        return latex_to_html_name(self.latex_name)

    @classmethod
    def empty(cls):
        # type: () -> Particle
        "Make a new empty particle."
        return cls(0, "Unknown", anti_flag=Inv.Same)

    @classmethod
    def from_pdgid(cls, value):
        # type: (SupportsInt) -> Particle
        """
        Get a particle from a PDGID. Uses by default the package
        extended PDG data table.

        Raises
        ------
        InvalidParticle
            If the input PDG ID is an invalid identification code.
        ParticleNotFound
            If no matching PDG ID is found in the loaded data table(s).
        """
        if not is_valid(value):
            raise InvalidParticle("Input PDGID {0} is invalid!".format(value))

        for item in cls.all():
            if item.pdgid == value:
                return item
        else:
            raise ParticleNotFound("Could not find PDGID {0}".format(value))

    @classmethod
    def findall(
        cls,
        filter_fn=None,  # type: Optional[Callable[[Particle], bool]]
        particle=None,  # type: Optional[bool]
        **search_terms  # type: Any
    ):
        # type: (...) -> List[Particle]
        """
        Search for a particle, returning a list of candidates.

        The first and only positional argument is given each particle
        candidate, and returns True/False. Example:

            >>> Particle.findall(lambda p: 'p' in p.name)    # doctest: +SKIP
            # Returns list of all particles with p somewhere in name

        You can pass particle=True/False to force a particle or antiparticle.
        If this is not callable, it will do a "fuzzy" search on the name. So this is identical:

            >>> Particle.findall('p')    # doctest: +SKIP
            # Returns list of all particles with p somewhere in name (same as example above)

        You can also pass keyword arguments, which are either called with the
        matching property if they are callable, or are compared if they are not.
        This would do an exact search on the name, instead of a fuzzy search:

           >>> # Returns proton and antiproton only
           >>> Particle.findall(pdg_name='p')    # doctest: +NORMALIZE_WHITESPACE
           [<Particle: name="p", pdgid=2212, mass=938.272081 ± 0.000006 MeV>,
            <Particle: name="p~", pdgid=-2212, mass=938.272081 ± 0.000006 MeV>,
            <Particle: name="p", pdgid=1000010010, mass=938.272081 ± 0.000006 MeV>,
            <Particle: name="p~", pdgid=-1000010010, mass=938.272081 ± 0.000006 MeV>]

           >>> # Returns proton only
           >>> Particle.findall(pdg_name='p', particle=True)    # doctest: +NORMALIZE_WHITESPACE
           [<Particle: name="p", pdgid=2212, mass=938.272081 ± 0.000006 MeV>,
           <Particle: name="p", pdgid=1000010010, mass=938.272081 ± 0.000006 MeV>]

        Versatile searches require a (lambda) function as argument:

        >>> # Get all neutral beauty hadrons
        >>> Particle.findall(lambda p: p.pdgid.has_bottom and p.charge==0)    # doctest: +SKIP
        >>>
        >>> # Trivially find all pseudoscalar charm mesons
        >>> Particle.findall(lambda p: p.pdgid.is_meson and p.pdgid.has_charm and p.spin_type==SpinType.PseudoScalar)  # doctest: +SKIP

        See also ``find``, which throws an exception if the particle is not found or too many are found.
        """

        # Note that particle can be called by position to keep compatibility with Python 2, but that behavior should
        # not be used and will be removed when support for Python 2.7 is dropped.

        results = set()

        # Filter out values
        for item in cls.all():
            # At this point, continue if a match fails

            # particle=True is particle, False is antiparticle, and None is both
            if particle is not None:
                if particle and int(item) < 0:
                    continue
                elif (not particle) and int(item) > 0:
                    continue

            # If a filter function is passed, evaluate and skip if False
            if filter_fn is not None:
                if callable(filter_fn):
                    # Just skip exceptions, which are there for good reasons
                    # Example: calls to Particle.ctau for particles given
                    #          default negative, and hence invalid, widths
                    try:
                        if not filter_fn(item):
                            continue
                    except TypeError:  # skip checks such as 'lambda p: p.width > 0',
                        continue  # which fail when width=None
                else:
                    if not (filter_fn in item.name):
                        continue

            # At this point, if you break, you will not add a match
            for term, value in search_terms.items():
                # If pvalue cannot be accessed, skip this particle
                # (invalid lifetime, for example)
                try:
                    pvalue = getattr(item, term)
                except ValueError:
                    break

                # Callables are supported
                if callable(value):
                    try:
                        if not value(pvalue):
                            break
                    except TypeError:  # catch issues with None values
                        break
                # And, finally, just compare if nothing else matched
                elif pvalue != value:
                    break

            # If the loop was not broken
            else:
                results.add(item)

        # Matches are sorted so the top one is "best"
        return sorted(results)

    @classmethod
    def find(cls, *args, **search_terms):
        # type: (...) -> Particle
        """
        Require that the search returns one and only one result.
        The method otherwise raises a ParticleNotFound or RuntimeError exception.

        See `findall` for full listing of parameters.

        Raises
        ------
        ParticleNotFound
            If no matching particle is found in the loaded data table(s).
        RuntimeError
            If too many particles match the search criteria.
        """

        results = cls.findall(*args, **search_terms)

        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            raise ParticleNotFound(
                "Did not find particle matching query: {}".format(search_terms)
            )
        else:
            raise RuntimeError("Found too many particles")

    @classmethod
    def from_evtgen_name(cls, name):
        # type: (str) -> Particle
        """
        Get a particle from an EvtGen particle name, as in .dec decay files.

        Raises
        ------
        ParticleNotFound
            If `from_pdgid` returns no match.
        MatchingIDNotFound
            If the matching EvtGen name - PDG ID done internally is unsuccessful.
        """
        return cls.from_pdgid(EvtGenName2PDGIDBiMap[name])

    @classmethod
    def from_string(cls, name):
        # type: (str) -> Particle
        "Get a particle from a PDG style name - returns the best match."
        matches = cls.from_string_list(name)
        if matches:
            return matches[0]
        else:
            raise ParticleNotFound("{0} not found in particle table".format(name))

    @classmethod
    def from_string_list(cls, name):
        # type: (str) -> List[Particle]
        "Get a list of particles from a PDG style name."

        # Forcible override
        particle = None

        short_name = name
        if "~" in name:
            short_name = name.replace("~", "")
            particle = False

        # Try the simplest searches first
        list_can = cls.findall(name=name, particle=particle)
        if list_can:
            return list_can
        else:
            list_can = cls.findall(pdg_name=short_name, particle=particle)
            if list_can:
                return list_can

        mat_str = getname.match(short_name)

        if mat_str is None:
            return []

        mat = mat_str.groupdict()

        if particle is False:
            mat["bar"] = "bar"

        try:
            return cls._from_group_dict_list(mat)
        except ParticleNotFound:
            return []

    @classmethod
    def _from_group_dict_list(cls, mat):
        # type: (Dict[str, Any]) -> List[Particle]

        kw = dict()  # type: Dict[str, Any]
        kw["particle"] = (
            False
            if mat["bar"] is not None
            else (True if mat["charge"] == "0" else None)
        )

        name = mat["name"]

        if mat["family"]:
            if "_" in mat["family"]:
                mat["family"] = mat["family"].strip("_")
            name += "({mat[family]})".format(mat=mat)
        if mat["state"]:
            name += "({mat[state]})".format(mat=mat)

        if "prime" in mat and mat["prime"]:
            name += "'"

        if mat["star"]:
            name += "*"

        if mat["state"] is not None:
            kw["J"] = float(mat["state"])

        if mat["mass"]:
            maxname = name + "({mat[mass]})".format(mat=mat)
        else:
            maxname = name

        if "charge" in mat and mat["charge"] is not None:
            kw["three_charge"] = Charge_mapping[mat["charge"]]

        vals = cls.findall(name=lambda x: maxname in x, **kw)
        if not vals:
            vals = cls.findall(name=lambda x: name in x, **kw)

        if not vals:
            raise ParticleNotFound(
                "Could not find particle {0} or {1}".format(maxname, name)
            )

        if len(vals) > 1 and mat["mass"] is not None:
            vals = [val for val in vals if mat["mass"] in val.latex_name]

        if len(vals) > 1:
            vals = sorted(vals)

        return vals
