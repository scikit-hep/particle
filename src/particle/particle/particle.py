# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

# Python standard library
import contextlib
import csv
from copy import copy
from functools import total_ordering
from typing import Any, Callable, Iterable, Iterator, Sequence, SupportsInt, TypeVar

# External dependencies
import attr
from hepunits.constants import c_light

from .. import data
from ..converters.evtgen import EvtGenName2PDGIDBiMap
from ..pdgid import PDGID, is_valid
from ..pdgid.functions import Location, _digit
from ..typing import HasOpen, HasRead, StringOrIO, Traversable
from .enums import (
    Charge,
    Charge_mapping,
    Charge_undo,
    Inv,
    Parity,
    Parity_undo,
    SpinType,
    Status,
)
from .kinematics import width_to_lifetime
from .regex import getname
from .utilities import latex_to_html_name, programmatic_name, str_with_unc

__all__ = ("Particle", "ParticleNotFound", "InvalidParticle")


def __dir__() -> tuple[str, ...]:
    return __all__


class ParticleNotFound(RuntimeError):
    pass


class InvalidParticle(RuntimeError):
    pass


def _isospin_converter(isospin: str) -> float | None:
    vals: dict[str | None, float | None] = {
        "0": 0.0,
        "1/2": 0.5,
        "1": 1.0,
        "3/2": 1.5,
    }
    return vals.get(isospin)


def _none_or_positive_converter(value: float) -> float | None:
    return None if value < 0 else value


# These are needed to trick attrs typing
minus_one: float | None = -1.0
none_float: float | None = None


Self = TypeVar("Self", bound="Particle")


@total_ordering
@attr.s(slots=True, eq=False, order=False, repr=False)
class Particle:
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

    pdgid: PDGID = attr.ib(converter=PDGID)
    pdg_name: str = attr.ib()
    mass: float | None = attr.ib(minus_one, converter=_none_or_positive_converter)
    mass_upper: float | None = attr.ib(minus_one, converter=_none_or_positive_converter)
    mass_lower: float | None = attr.ib(minus_one, converter=_none_or_positive_converter)
    width: float | None = attr.ib(minus_one, converter=_none_or_positive_converter)
    width_upper: float | None = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )
    width_lower: float | None = attr.ib(
        minus_one, converter=_none_or_positive_converter
    )
    _three_charge: Charge | None = attr.ib(Charge.u, converter=Charge)  # charge * 3
    I: float | None = attr.ib(none_float, converter=_isospin_converter)  # noqa: E741
    # J = attr.ib(None)  # Total angular momentum
    G = attr.ib(Parity.u, converter=Parity)  # Parity: '', +, -, or ?
    P = attr.ib(Parity.u, converter=Parity)  # Space parity
    C = attr.ib(Parity.u, converter=Parity)  # Charge conjugation parity
    anti_flag = attr.ib(
        Inv.Same, converter=Inv
    )  # Info about particle name for anti-particles
    rank: int = attr.ib(0)
    status = attr.ib(Status.NotInPDT, converter=Status)
    quarks = attr.ib("", converter=str)
    latex_name: str = attr.ib("Unknown")

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: name="{self}", pdgid={int(self.pdgid)}, mass={self._str_mass()}>'

    # Ordered loaded table of entries
    _table: list[Particle] | None = None

    # Hash optimized table of particles
    _hash_table: dict[int, Particle] | None = None

    # Names of loaded tables
    _table_names: list[str] | None = None

    @classmethod
    def table_names(cls) -> tuple[str, ...]:
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

        return ()

    @classmethod
    def table_loaded(cls) -> bool:
        """
        Check to see if the table is loaded.
        """
        return cls._table is not None

    @classmethod
    def all(cls: type[Self]) -> list[Self]:
        """
        Access, hence get hold of, the internal particle data CSV table,
        loading it from the default location if no table has yet been loaded.
        All `Particle` (instances) are returned as a list.
        """
        if not cls.table_loaded():
            cls.load_table()

        return cls._table if cls._table is not None else []  # type: ignore[return-value]

    @classmethod
    def to_list(
        cls,
        exclusive_fields: Iterable[str] = (),
        exclude_fields: Iterable[str] = (),
        n_rows: int = -1,
        filter_fn: Callable[[Particle], bool] | None = None,
        particle: bool | None = None,
        **search_terms: Any,
    ) -> Sequence[Sequence[bool | int | float | str]]:
        """
        Render a search (via `findall`) on the internal particle data CSV table
        as a `list`, loading the table from the default location if no table has yet been loaded.

        The returned attributes are those of the class. By default all attributes
        are used as fields. Their complete list is:
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

        It is possible to add as returned fields any `Particle` class property,
        e.g. 'name', `J` or `ctau`, see examples below.

        Parameters
        ----------
        exclusive_fields: list, optional, default is []
            Exclusive list of fields to print out,
            which can be any `Particle` class property.
        exclude_fields: list, optional, default is []
            List of table fields to exclude in the printout.
            Relevant only when exclusive_fields is not given.
        n_rows: int, optional, defaults to all rows
            Number of table rows to print out.
        filter_fn: function, optional, default is None
            Apply a filter to each particle.
            See `findall(...)`` for typical use cases.
        particle: bool, optional, default is None
            Pass particle=True/False to only return particles or antiparticles.
            Option passed on internally to `findall(...)``.
        search_terms: keyword arguments, optional
            See `findall(...)`` for typical use cases.

        Returns
        -------
        The particle table query as a `list`.

        Note
        ----
        The `tabulate` package is suggested as a means to print-out
        the contents of the query as a nicely formatted table.

        Examples
        --------
        Reproduce the whole particle table kept internally:

        >>> query_as_list = Particle.to_list()

        Reduce the information on the particle table to the only fields
        ['pdgid', 'pdg_name'] and render the first 5 particles:

        >>> query_as_list = Particle.to_list(exclusive_fields=['pdgid', 'pdg_name'], n_rows=5)
        >>> from tabulate import tabulate
        >>> print(tabulate(query_as_list, headers='firstrow'))
          pdgid  pdg_name
        -------  ----------
              1  d
             -1  d
              2  u
             -2  u
              3  s

        Request the properties of a specific list of particles:

        >>> query_as_list = Particle.to_list(filter_fn=lambda p: p.pdgid.is_lepton and p.charge!=0, exclusive_fields=['pdgid', 'name', 'mass', 'charge'], particle=False)
        >>> print(tabulate(query_as_list, headers='firstrow', tablefmt="rst", floatfmt=".12g", numalign="decimal"))
        =======  ======  ===============  ========
          pdgid  name               mass    charge
        =======  ======  ===============  ========
            -11  e+         0.5109989461         1
            -13  mu+      105.6583745            1
            -15  tau+    1776.86                 1
            -17  tau'+                           1
        =======  ======  ===============  ========

        >>> query_as_list = Particle.to_list(filter_fn=lambda p: p.pdgid.is_lepton, pdg_name='tau', exclusive_fields=['pdgid', 'name', 'mass', 'charge'])
        >>> print(tabulate(query_as_list, headers='firstrow'))
          pdgid  name       mass    charge
        -------  ------  -------  --------
             15  tau-    1776.86        -1
            -15  tau+    1776.86         1

        Save it to a file:

        >>> with open('particles.txt', "w") as outfile:    # doctest: +SKIP
        ...    print(tabulate(query_as_list, headers='firstrow', tablefmt="rst", floatfmt=".12g", numalign="decimal"), file=outfile)    # doctest: +SKIP
        """
        if not cls.table_loaded():
            cls.load_table()

        # Get all table headers from the class attributes
        tbl_names = [a.name for a in attr.fields(Particle)]
        # ... and replace '_three_charge' with the better, public property
        tbl_names[tbl_names.index("_three_charge")] = "three_charge"

        list_exclusive_fields = list(exclusive_fields)
        if list_exclusive_fields:
            tbl_names = list_exclusive_fields
        else:
            for fld in exclude_fields:
                with contextlib.suppress(ValueError):
                    tbl_names.remove(fld)

        # Start with the full table
        tbl_all = sorted(cls.all())

        # Apply a filter, if specified
        if filter_fn is not None:
            tbl_all = cls.findall(filter_fn, particle=particle, **search_terms)

        # In any case, only keep a given number of rows?
        if n_rows >= 0:
            tbl_all = tbl_all[:n_rows]

        # Build all table rows
        tbl = [tbl_names]
        for p in tbl_all:
            tbl.append([getattr(p, attr) for attr in tbl_names])

        return tbl

    @classmethod
    def to_dict(
        cls, *args: Any, **kwargs: Any
    ) -> dict[str, tuple[bool | int | str | float, ...]]:
        """
        Render a search (via `findall`) on the internal particle data CSV table
        as a `dict`, loading the table from the default location if no table has yet been loaded.

        See `to_list` for details on the full function signature.

        The returned attributes are those of the class. By default all attributes
        are used as fields. Their complete list is:
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

        It is possible to add as returned fields any `Particle` class property,
        e.g. 'name', `J` or `ctau`, see examples below.

        Parameters
        ----------
        exclusive_fields: list, optional, default is []
            Exclusive list of fields to print out,
            which can be any `Particle` class property.
        exclude_fields: list, optional, default is []
            List of table fields to exclude in the printout.
            Relevant only when exclusive_fields is not given.
        n_rows: int, optional, defaults to all rows
            Number of table rows to print out.
        filter_fn: function, optional, default is None
            Apply a filter to each particle.
            See `findall(...)`` for typical use cases.
        particle: bool, optional, default is None
            Pass particle=True/False to only return particles or antiparticles.
            Option passed on internally to `findall(...)``.
        search_terms: keyword arguments, optional
            See `findall(...)`` for typical use cases.

        Returns
        -------
        The particle table query as a `dict`.

        Note
        ----
        The `tabulate` package is suggested as a means to print-out
        the contents of the query as a nicely formatted table.

        Examples
        --------
        Reproduce the whole particle table kept internally:

        >>> query_as_dict = Particle.to_dict()

        Reduce the information on the particle table to the only fields
        ['pdgid', 'pdg_name'] and render the first 5 particles:

        >>> query_as_dict = Particle.to_dict(exclusive_fields=['pdgid', 'pdg_name'], n_rows=5)
        >>> from tabulate import tabulate    # doctest: +SKIP
        >>> print(tabulate(query_as_dict, headers='keys'))    # doctest: +SKIP
          pdgid  pdg_name
        -------  ----------
              1  d
             -1  d
              2  u
             -2  u
              3  s

        Request the properties of a specific list of particles:

        >>> query_as_dict = Particle.to_dict(filter_fn=lambda p: p.pdgid.is_lepton and p.charge!=0, exclusive_fields=['pdgid', 'name', 'mass', 'charge'], particle=True)
        >>> print(tabulate(query_as_dict, headers='keys', tablefmt="rst", floatfmt=".12g", numalign="decimal"))    # doctest: +SKIP
        =======  ======  ===============  ========
          pdgid  name               mass    charge
        =======  ======  ===============  ========
             11  e-         0.5109989461        -1
             13  mu-      105.6583745           -1
             15  tau-    1776.86                -1
             17  tau'-                          -1
        =======  ======  ===============  ========

        >>> query_as_dict = Particle.to_dict(filter_fn=lambda p: p.pdgid.is_lepton, pdg_name='tau', exclusive_fields=['pdgid', 'name', 'mass', 'charge'])
        >>> print(tabulate(query_as_dict, headers='keys'))    # doctest: +SKIP
          pdgid  name       mass    charge
        -------  ------  -------  --------
             15  tau-    1776.86        -1
            -15  tau+    1776.86         1

        Save it to a file:

        >>> with open('particles.txt', "w") as outfile:    # doctest: +SKIP
        ...    print(tabulate(query_as_dict, headers='keys', tablefmt="rst", floatfmt=".12g", numalign="decimal"), file=outfile)    # doctest: +SKIP
        """
        query_as_list = cls.to_list(*args, **kwargs)
        headers = query_as_list[0]
        rows = zip(*query_as_list[1:])

        return {str(h): r for h, r in zip(headers, rows)}

    @classmethod
    def load_table(
        cls,
        filename: StringOrIO | None = None,
        append: bool = False,
        _name: str | None = None,
    ) -> None:
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
            cls._table = []
            cls._hash_table = {}
            cls._table_names = []

        # Tell MyPy that this is true
        assert cls._table is not None
        assert cls._hash_table is not None
        assert cls._table_names is not None

        if filename is None:
            with data.basepath.joinpath("particle2022.csv").open() as fa:
                cls.load_table(fa, append=append, _name="particle2022.csv")
            with data.basepath.joinpath("nuclei2020.csv").open() as fb:
                cls.load_table(fb, append=True, _name="nuclei2020.csv")
            return
        if isinstance(filename, HasRead):
            tmp_name = _name or filename.name
            cls._table_names.append(tmp_name or f"{filename!r} {len(cls._table_names)}")
            open_file = filename
        elif isinstance(filename, HasOpen):
            cls._table_names.append(str(filename))
            open_file = filename.open()
        else:
            cls._table_names.append(str(filename))
            assert not isinstance(filename, Traversable)
            open_file = open(filename, encoding="utf_8")

        with open_file as f:
            r = csv.DictReader(line for line in f if not line.startswith("#"))

            for v in r:
                with contextlib.suppress(ValueError):
                    value = int(v["ID"])

                    p = cls(
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

                    # Replace the previous value if it exists
                    cls._hash_table[value] = p

        cls._table = sorted(cls._hash_table.values())

    # The following __le__ and __eq__ needed for total ordering (sort, etc)

    def __lt__(self, other: Particle | int) -> bool:
        # Sort by absolute particle numbers
        # The positive one should come first
        if isinstance(other, Particle):
            return abs(int(self.pdgid) - 0.25) < abs(int(other.pdgid) - 0.25)
        # Comparison with anything else should produce normal comparisons.
        return int(self.pdgid) < other

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Particle):
            return self.pdgid == other.pdgid
        return self.pdgid == other

    # Only one particle can exist per PDGID number
    def __hash__(self) -> int:
        return hash(self.pdgid)

    # Shared with PDGID

    @property
    def J(self) -> int:
        """
        The total spin J quantum number.

        Note that the returned value corresponds to that effectively encoded
        in the particle PDG ID.
        """
        return self.pdgid.J  # type: ignore[no-any-return]

    @property
    def L(self) -> int | None:
        """
        The orbital angular momentum L quantum number (None if not a meson).

        Note that the returned value corresponds to that effectively encoded
        in the particle PDG ID.
        """
        return self.pdgid.L  # type: ignore[no-any-return]

    @property
    def S(self) -> int | None:
        """
        The spin S quantum number (None if not a meson).

        Note that the returned value corresponds to that effectively encoded
        in the particle PDG ID.
        """
        return self.pdgid.S  # type: ignore[no-any-return]

    @property
    def charge(self) -> float | None:
        """
        The particle charge, in units of the positron charge.

        Design note: the particle charge can also be retrieved from the particle PDG ID.
        To allow for user-defined particles, it is necessary to rather store
        the particle charge in the data tables themselves.
        Consistency of both ways of retrieving the particle charge is guaranteed
        for all PDG table particles.
        """
        return self.three_charge / 3 if self.three_charge is not None else None

    @property
    def three_charge(self) -> int | None:
        "Three times the particle charge (charge * 3), in units of the positron charge."
        if not self.pdgid.is_nucleus:
            # Return int(...) not to return the actual enum Charge
            return (
                int(self._three_charge)
                if self._three_charge is not None and self._three_charge != Charge.u
                else None
            )

        return self.pdgid.three_charge  # type: ignore[no-any-return]

    @property
    def lifetime(self) -> float | None:
        """
        The particle lifetime, in nanoseconds.

        None is returned if the particle width (stored in the DB) is unknown.
        """
        return width_to_lifetime(self.width) if self.width is not None else None

    @property
    def ctau(self) -> float | None:
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
    def is_name_barred(self) -> bool:
        """
        Check to see if particle is inverted (hence is it an antiparticle)
        and has a bar in its name.
        """
        return self.pdgid < 0 and self.anti_flag == Inv.Barred

    @property
    def spin_type(self) -> SpinType:
        """
        Access the SpinType enum.

        Note that this is relevant for bosons only. SpinType.NonDefined is returned otherwise.
        """
        # Non-valid or non-standard PDG IDs
        if self.pdgid.j_spin is None:
            return SpinType.NonDefined

        # Fermions - 2J+1 is always an even number
        if self.pdgid.j_spin % 2 == 0:
            return SpinType.NonDefined

        J = int(self.J)
        if J in {0, 1, 2}:
            if self.P == Parity.p:
                return (SpinType.Scalar, SpinType.Axial, SpinType.Tensor)[J]
            if self.P == Parity.m:
                spin_types = (
                    SpinType.PseudoScalar,
                    SpinType.Vector,
                    SpinType.PseudoTensor,
                )
                return spin_types[J]

        return SpinType.Unknown

    @property
    def is_self_conjugate(self) -> bool:
        """
        Is the particle self-conjugate, i.e. its own antiparticle?
        """
        return self.anti_flag == Inv.Same

    @property
    def is_unflavoured_meson(self) -> bool:
        """
        Is the particle a light non-strange meson or a quarkonium?

        Indeed, unflavoured mesons are either:
        all light mesons with no net flavour quantum number (S = C = B = T = 0),
        or quarkonia, which are self-conjugate heavy flavour mesons,
        with all their flavour quantum numbers and charge equal to zero.
        """
        pid = self.pdgid

        if not pid.is_meson:
            return False

        # Heavy flavour
        if pid.has_charm or pid.has_bottom or pid.has_top:
            return self.is_self_conjugate

        # Light or strange mesons at this point

        # Special case of the KS and KL
        if pid in {130, 310}:
            return False

        # I = 1 light mesons have no s-sbar component, hence has_strange == False
        if _digit(pid, Location.Nq3) == 1 and not pid.has_strange:
            return True

        # I = 0 light mesons have a s-sbar component, has_strange == True,
        # thought their net S = 0
        if _digit(pid, Location.Nq3) in {2, 3} and self.three_charge == 0:
            return True

        # Only K-mesons at this point
        return False

    def invert(self: Self) -> Self:
        "Get the antiparticle."
        if self.anti_flag == Inv.Barred or (
            self.anti_flag == Inv.ChargeInv and self.three_charge != Charge.o
        ):
            return self.from_pdgid(-self.pdgid)
        return copy(self)

    __neg__ = invert
    __invert__ = invert

    # Pretty descriptions

    def __str__(self) -> str:
        _tilde = "~" if self.anti_flag == Inv.Barred and self.pdgid < 0 else ""
        _charge = self._str_charge() if self._charge_in_name() else ""
        return self.pdg_name + _tilde + _charge

    name = property(
        __str__,
        doc="The nice name, with charge added, and a tilde for an antiparticle, if relevant.",
    )

    def _repr_latex_(self) -> str:
        name = self.latex_name
        return ("$" + name + "$") if self.latex_name else "?"

    def _width_or_lifetime(self) -> str:
        """
        Display either the particle width or the lifetime.
        Internally used by the describe() method.

        Note
        ----
        Width errors equal to None flag an experimental upper limit on the width.
        """
        if self.width is None:
            return "Width = None"
        if self.width == 0:
            return "Width = 0.0 MeV"
        if self.width_lower is None or self.width_upper is None:
            return f"Width < {self.width} MeV"
        if (
            self.width < 0.05
        ):  # corresponds to a lifetime of approximately 1.3e-20 seconds
            assert self.lifetime is not None
            if self.width_lower != self.width_upper:
                lifetime = str_with_unc(
                    self.lifetime,
                    width_to_lifetime(self.width - self.width_lower) - self.lifetime,
                    self.lifetime - width_to_lifetime(self.width + self.width_upper),
                )
                return f"Lifetime = {lifetime} ns"

            e = width_to_lifetime(self.width - self.width_lower) - self.lifetime
            lifetime = str_with_unc(self.lifetime, e, e)
            return f"Lifetime = {lifetime} ns"

        width = str_with_unc(self.width, self.width_upper, self.width_lower)
        return f"Width = {width} MeV"

    def _charge_in_name(self) -> bool:
        """Assess whether the particle charge is part of the particle name.

        Internally used when creating the name.
        """
        if self.anti_flag == Inv.ChargeInv:
            return True  # antiparticle flips sign of particle
        if self.pdgid in (23, 25, 111, 130, 310, 311, -311):
            return True  # the Z0, H0, pi0, KL0, KS0, K0 and K0bar
        if self.pdgid.is_diquark:
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
            if any(
                chr in self.pdg_name
                for chr in ("eta", "h(", "h'(", "omega", "phi", "f", "f'")
            ):
                return False
            if pid.has_strange or pid.has_charm or pid.has_bottom or pid.has_top:
                return False

            # Light unflavoured mesons
            return True
        # Lambda baryons
        if (
            self.pdgid.is_baryon
            and _digit(self.pdgid, Location.Nq2) == 1
            and self.I
            == 0.0  # 1st check alone is not sufficient to filter out lowest-ground Sigma's
            and self.pdgid.has_strange
            and not (
                self.pdgid.has_charm or self.pdgid.has_bottom or self.pdgid.has_top
            )
        ):
            return False
        if self.pdgid.is_nucleus:
            return False
        return True

    def _str_charge(self) -> str:
        """
        Display a reasonable particle charge printout.
        Internally used by the describe() and __str__ methods.
        """
        if self._three_charge is None:
            return "None"
        if not self.pdgid.is_nucleus:
            return Charge_undo[Charge(self._three_charge)]

        return str(self.pdgid.charge)

    def _str_mass(self) -> str:
        """
        Display a reasonable particle mass printout
        even when no mass value is available.
        Internally used by the describe() method.
        """
        if self.mass is None:
            return "None"

        txt = str_with_unc(self.mass, self.mass_upper, self.mass_lower)
        return f"{txt} MeV"

    def describe(self) -> str:
        "Make a nice high-density string for a particle's properties."

        if self.pdgid == 0:
            return "Name: Unknown"

        G = Parity_undo[self.G]
        C = Parity_undo[self.C]
        Q = self._str_charge()
        P = Parity_undo[self.P]
        mass = self._str_mass()
        width_or_lifetime = self._width_or_lifetime()
        latex_name = self._repr_latex_()

        val = f"""Name: {self!s:<14} ID: {self.pdgid:<12} Latex: {latex_name}
Mass  = {mass}
{width_or_lifetime}
Q (charge)        = {Q:<6}  J (total angular) = {self.J!s:<7}  P (space parity) = {P}
C (charge parity) = {C:<6}  I (isospin)       = {self.I!s:<7}  G (G-parity)     = {G}
"""

        if self.spin_type != SpinType.Unknown:
            val += f"    SpinType: {self.spin_type!s}\n"
        if self.quarks:
            val += f"    Quarks: {self.quarks}\n"
        val += f"    Antiparticle name: {self.invert().name} (antiparticle status: {self.anti_flag.name})"
        return val

    @property
    def evtgen_name(self) -> str:
        "This is the name used in EvtGen."
        return EvtGenName2PDGIDBiMap[self.pdgid]

    @property
    def programmatic_name(self) -> str:
        "This name could be used for a variable name."
        return programmatic_name(self.name)

    @property
    def html_name(self) -> str:
        "This is the name in HTML."
        return latex_to_html_name(self.latex_name)

    @classmethod
    def empty(cls: type[Self]) -> Self:
        "Make a new empty particle."
        return cls(0, "Unknown", anti_flag=Inv.Same)

    @classmethod
    def from_pdgid(cls: type[Self], value: SupportsInt) -> Self:
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
            raise InvalidParticle(f"Input PDGID {value} is invalid!")

        if not cls.table_loaded():
            cls.load_table()

        assert cls._hash_table is not None

        try:
            return cls._hash_table[int(value)]  # type: ignore[return-value]
        except KeyError:
            raise ParticleNotFound(f"Could not find PDGID {value}") from None

    @classmethod
    def from_name(cls: type[Self], name: str) -> Self:
        """
        Get a particle from its name.

        Raises
        ------
        ParticleNotFound
            If no particle matches the input name.
        """
        try:
            (particle,) = cls.finditer(
                name=name
            )  # throws an error if < 1 or > 1 particle is found
            return particle
        except ValueError:
            raise ParticleNotFound(f'Could not find name "{name}"') from None

    @classmethod
    def from_evtgen_name(cls: type[Self], name: str) -> Self:
        """
        Get a particle from an EvtGen particle name, as in .dec decay files.

        Raises
        ------
        ParticleNotFound
            If `from_pdgid`, internally called, returns no match.
        MatchingIDNotFound
            If the matching EvtGen name - PDG ID done internally is unsuccessful.
        """
        return cls.from_pdgid(EvtGenName2PDGIDBiMap[name])

    @classmethod
    def from_nucleus_info(
        cls: type[Self],
        z: int,
        a: int,
        anti: bool = False,
        i: int = 0,
        l_strange: int = 0,
    ) -> Self:
        """
        Get a nucleus particle from the proton Z and atomic mass A numbers.

        As described in the PDG numbering scheme:
        "To avoid ambiguities, nucleus codes should not be applied to a single hadron, such as the p, n
        or the Λ, where quark-contents-based codes already exist."

        Number of neutrons is equal to a-z.
        The PDG ID format is ±10LZZZAAAI, see the `is_nucleus()` function in submodule
        `particle.pdgid.functions.py`.

        Parameters
        ----------
        z: int
            Atomic number Z (number of protons).
            Maximum three decimal digits.
        a: int
            Atomic mass number A (total number of baryons).
            Maximum three decimal digits.
        anti: bool, optional, defaults to False (not antimatter).
            Whether the nucleus should be antimatter.
        i: int, optional, default is 0
            Isomer level I. I=0 corresponds to the ground-state.
            I>0 are excitations.
            Maximum is one decimal digit.
        l_strange: int, optional, default is 0
            Total number of strange quarks.
            Maximum is one decimal digit.

        Raises
        ------
        ParticleNotFound
            If `from_pdgid`, internally called, returns no match.
        InvalidParticle
            If the input combination is invalid.
        """
        if l_strange < 0 or l_strange > 9:
            raise InvalidParticle(
                f"Number of strange quarks l={l_strange} is invalid. Must be 0 <= l <= 9."
            )
        if z < 0 or z > 999:
            raise InvalidParticle(
                f"Atomic number Z={z} is invalid. Must be 0 <= A <= 999."
            )
        if a < 0 or a > 999:
            raise InvalidParticle(
                f"Atomic mass number A={a} is invalid. Must be 0 <= A <= 999."
            )
        if i < 0 or i > 9:
            raise InvalidParticle(
                f"Isomer level I={i} is invalid. Must be 0 <= I <= 9."
            )
        if z > a:
            raise InvalidParticle(
                f"Nucleus A={a}, Z={z} is invalid. Z must be smaller or equal to Z."
            )

        pdgid = int(1e9 + l_strange * 1e5 + z * 1e4 + a * 10 + i)

        if anti:
            return cls.from_pdgid(-pdgid)

        return cls.from_pdgid(pdgid)

    @classmethod
    def finditer(
        cls: type[Self],
        filter_fn: Callable[[Particle], bool] | str | None = None,
        *,
        particle: bool | None = None,
        **search_terms: Any,
    ) -> Iterator[Self]:
        """
        Search for a particle, returning an iterator of candidates.

        The first and only positional argument is given to each particle
        candidate, and returns True/False. Example:

            >>> Particle.finditer(lambda p: 'p' in p.name)    # doctest: +SKIP
            # Returns iterator of all particles with p somewhere in name

        You can pass particle=True/False to force a particle or antiparticle.
        If this is not callable, it will do a "fuzzy" search on the name. So this is identical:

            >>> Particle.finditer('p')    # doctest: +SKIP
            # Returns literator of all particles with p somewhere in name (same as example above)

        You can also pass keyword arguments, which are either called with the
        matching property if they are callable, or are compared if they are not.
        This would do an exact search on the name, instead of a fuzzy search:

           >>> # Returns proton and antiproton only
           >>> Particle.finditer(pdg_name='p')    # doctest: +SKIP
           # Returns iterator

           >>> # Returns proton only
           >>> Particle.finditer(pdg_name='p', particle=True)    # doctest: +SKIP
           # Returns iterator

        Versatile searches require a (lambda) function as argument:

        >>> # Get all neutral beauty hadrons
        >>> Particle.finditer(lambda p: p.pdgid.has_bottom and p.charge==0)    # doctest: +SKIP
        >>>
        >>> # Trivially find all pseudoscalar charm mesons
        >>> Particle.finditer(lambda p: p.pdgid.is_meson and p.pdgid.has_charm and p.spin_type==SpinType.PseudoScalar)  # doctest: +SKIP

        See also ``findall``, which returns the same thing, but as a list.
        """

        # Filter out values
        for item in cls.all():
            # At this point, continue if a match fails

            # particle=True is particle, False is antiparticle, and None is both
            if particle is not None:
                if particle and int(item.pdgid) < 0:
                    continue
                if (not particle) and int(item.pdgid) > 0:
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
                elif filter_fn not in item.name:
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
                yield item

    @classmethod
    def findall(
        cls: type[Self],
        filter_fn: Callable[[Particle], bool] | None = None,
        *,
        particle: bool | None = None,
        **search_terms: Any,
    ) -> list[Self]:

        """
        Search for a particle, returning a list of candidates.

        The first and only positional argument is given to each particle
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

        See also ``finditer``, which provides an iterator instead of a list.
        """

        return list(
            cls.finditer(filter_fn=filter_fn, particle=particle, **search_terms)
        )

    @classmethod
    def find(cls: type[Self], *args: Any, **search_terms: Any) -> Self:
        raise AttributeError(
            "Method has been removed post versions 0.16. Please use finditer or findall instead."
        )

    @classmethod
    def from_string(cls: type[Self], name: str) -> Self:
        "Get a particle from a PDG style name - returns the best match."
        matches = cls.from_string_list(name)
        if matches:
            return matches[0]
        raise ParticleNotFound(f"{name} not found in particle table")

    @classmethod
    def from_string_list(cls: type[Self], name: str) -> list[Self]:
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
    def _from_group_dict_list(cls: type[Self], mat: dict[str, Any]) -> list[Self]:

        kw: dict[str, Any] = {
            "particle": False
            if mat["bar"] is not None
            else True
            if mat["charge"] == "0"
            else None
        }

        name = mat["name"]

        if mat["family"]:
            if "_" in mat["family"]:
                mat["family"] = mat["family"].strip("_")
            name += f'({mat["family"]})'
        if mat["state"]:
            name += f'({mat["state"]})'

        if "prime" in mat and mat["prime"]:
            name += "'"

        if mat["star"]:
            name += "*"

        if mat["state"] is not None:
            kw["J"] = float(mat["state"])

        maxname = name + f'({mat["mass"]})' if mat["mass"] else name
        if "charge" in mat and mat["charge"] is not None:
            kw["three_charge"] = Charge_mapping[mat["charge"]]

        vals = cls.findall(name=lambda x: maxname in x, **kw)
        if not vals:
            vals = cls.findall(name=lambda x: name in x, **kw)

        if not vals:
            raise ParticleNotFound(f"Could not find particle {maxname} or {name}")

        if len(vals) > 1 and mat["mass"] is not None:
            vals = [val for val in vals if mat["mass"] in val.latex_name]

        if len(vals) > 1:
            vals = sorted(vals)

        return vals
