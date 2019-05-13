# -*- encoding: utf-8 -*-
# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import, division, print_function

# Python standard library
import operator
import os
import re
import csv
from copy import copy

from fractions import Fraction
from functools import reduce, total_ordering

# External dependencies
import attr

from hepunits.constants import c_light

from .. import data
from ..pdgid import PDGID
from ..pdgid import is_valid
from ..pdgid.functions import _digit
from ..pdgid.functions import Location
from .regex import getname, getdec

from .enums import (SpinType, Parity, Charge, Inv, Status,
                    Parity_undo, Parity_prog,
                    Charge_undo, Charge_prog, Charge_mapping)

from .utilities import (programmatic_name, str_with_unc,
                        latex_to_html_name)

from .kinematics import width_to_lifetime


class ParticleNotFound(RuntimeError):
    pass


class InvalidParticle(RuntimeError):
    pass


@total_ordering
@attr.s(slots=True, cmp=False, repr=False)
class Particle(object):
    """
    The Particle object class. Hold a series of properties for a particle.

    Class properties:

    C
        The charge conjugation parity quantum number, if relevant.

    G
        The G-parity quantum number, if relevant.

    I
        The isospin quantum number, if relevant.

    P
        The parity quantum number, if relevant.

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
    mass = attr.ib()
    width = attr.ib()
    anti_flag = attr.ib(converter=Inv)  # Info about particle name for anti-particles
    _three_charge = attr.ib(Charge.u, converter=Charge)  # charge * 3
    rank = attr.ib(0)  # Next line is Isospin
    I = attr.ib(None)  # noqa: E741
    # J = attr.ib(None)  # Total angular momentum
    G = attr.ib(Parity.u, converter=Parity)  # Parity: '', +, -, or ?
    P = attr.ib(Parity.u, converter=Parity)  # Space parity
    C = attr.ib(Parity.u, converter=Parity)  # Charge conjugation parity
    quarks = attr.ib('', converter=str)
    status = attr.ib(Status.Nonexistent, converter=Status)
    latex_name = attr.ib('Unknown')
    mass_upper = attr.ib(0.0)
    mass_lower = attr.ib(0.0)
    width_upper = attr.ib(0.0)
    width_lower = attr.ib(0.0)

    def __repr__(self):
        return '<{self.__class__.__name__}: name="{self!s}", pdgid={pdgid}, mass={mass} MeV>'.format(
            self=self, pdgid=int(self.pdgid),
            mass=str_with_unc(self.mass, self.mass_upper, self.mass_lower))

    _table = None # Loaded table of entries
    _table_names = None # Names of loaded tables

    @classmethod
    def table_names(cls):
        """
        Return the list of names loaded (will load the table, check with table_loaded() first if you don't want to load).
        """

        if cls._table_names is None:
            cls.load_table()

        return tuple(cls._table_names) # make a copy to avoid user manipulation

    @classmethod
    def table_loaded(cls):
        """
        Check to see if the table is loaded.
        """
        return not cls._table is None

    @classmethod
    def table(cls):
        """
        This accesses the internal particle data CSV table, loading it from the default location if needed.
        """
        if not cls.table_loaded():
            cls.load_table()

        return cls._table

    @classmethod
    def load_table(cls, filename=None, append=False):
        """
        Load a particle data CSV table. Optionally append to the existing data already loaded if append=True.
        As a special case, if this is called with append=True and the table is not loaded, the default will
        be loaded first before appending (set append=False if you don't want this behavior).
        """
        if append and not cls.table_loaded():
            cls.load_table(append=False) # default load
        elif not append:
            cls._table = []
            cls._table_names = []

        if filename is None:
            filename = data.open_text(data, 'particle2018.csv')
            cls._table_names.append('particle2018.csv')
        elif not hasattr(filename, 'read'):
            # Conversion to handle pathlib on Python < 3.6:
            filename = str(filename)
            cls._table_names.append(filename)
            filename = open(filename)
        else:
            cls._table_names.append('{0!r} {1}'.format(filename, len(cls._table_names)))

        with filename as f:
            r = csv.DictReader(f)

            for v in r:
                value = int(v['ID'])
                pdg_name = v['Name']

                # Replace the previous value if appending
                if value in cls._table:
                    cls._table.remove(value)

                cls._table.append(cls(
                    pdgid=value,
                    mass=float(v['Mass']),
                    mass_upper=float(v['MassUpper']),
                    mass_lower=float(v['MassLower']),
                    width=float(v['Width']),
                    width_upper=float(v['WidthUpper']),
                    width_lower=float(v['WidthLower']),
                    I=v['I'],
                    G=int(v['G']),
                    P=int(v['P']),
                    C=int(v['C']),
                    anti_flag=int(v['Anti']),
                    three_charge=int(v['Charge']),
                    rank=int(v['Rank']),
                    status=int(v['Status']),
                    pdg_name=v['Name'],
                    quarks=v['Quarks'],
                    latex_name=v['Latex']))

    # The following __le__ and __eq__ needed for total ordering (sort, etc)

    def __le__(self, other):
        # Sort by absolute particle numbers
        # The positive one should come first
        if type(self) == type(other):
            return abs(int(self) - .25) < abs(int(other) - .25)

        # Comparison with anything else should produce normal comparisons.
        else:
            return int(self) < other

    def __eq__(self, other):
        try:
            return self.pdgid == other.pdgid
        except AttributeError:
            return self.pdgid == other

    # Only one particle can exist per PDGID number
    def __hash__(self):
        return hash(self.pdgid)

    # Integer == PDGID
    def __int__(self):
        return int(self.pdgid)

    # Shared with PDGID

    @property
    def J(self):
        'The total spin J quantum number.'
        return self.pdgid.J

    @property
    def L(self):
        'The orbital angular momentum L quantum number (None if not a meson).'
        return self.pdgid.L

    @property
    def S(self):
        'The spin S quantum number (None if not a meson).'
        return self.pdgid.S

    @property
    def charge(self):
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
    def three_charge(self):
        'Three times the particle charge (charge * 3), in units of the positron charge.'
        return int(self._three_charge) if self._three_charge!=Charge.u else None

    @property
    def lifetime(self):
        'The particle lifetime, in nanoseconds.'
        return width_to_lifetime(self.width)

    @property
    def ctau(self):
        'The particle c*tau, in millimeters.'
        return c_light*self.lifetime

    @property
    def is_name_barred(self):
        """
        Check to see if particle is inverted (hence is it an antiparticle)
        and has a bar in its name.
        """
        return self.pdgid < 0 and self.anti_flag == Inv.Barred

    @property
    def spin_type(self):  # -> SpinType:
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

        if self.J in [0, 1, 2]:
            J = int(self.J)

            if self.P == Parity.p:
                return (SpinType.Scalar, SpinType.Axial, SpinType.Tensor)[J]
            elif self.P == Parity.m:
                return (SpinType.PseudoScalar, SpinType.Vector, SpinType.PseudoTensor)[J]

        return SpinType.Unknown

    @property
    def is_self_conjugate(self):
        """
        Is the particle self-conjugate, i.e. its own antiparticle?
        """
        return self.anti_flag == Inv.Same

    def invert(self):
        "Get the antiparticle."
        if self.anti_flag == Inv.Barred or (self.anti_flag == Inv.ChargeInv and self.three_charge != Charge.o):
            return self.from_pdgid(-self.pdgid)
        else:
            return copy(self)

    __neg__ = invert
    __invert__ = invert

    def _charge_in_name(self):
        """Assess whether the particle charge is part of the particle name.

        Internally used when creating the name.
        """
        if self.anti_flag == Inv.ChargeInv: return True   # antiparticle flips sign of particle
        if self.pdgid in (23, 25, 111, 130, 310, 311, -311): return True  # the Z0, H0, pi0, KL0, KS0, K0 and K0bar
        if abs(self.pdgid) in (2212, 2112): return False   # proton and neutron
        if self.three_charge == 0 and self.anti_flag == Inv.Same: return False   # all quarkonia and the photon
        if self.pdgid in (9000113, 9010113): return True  # special particles not yet well-known in the 2018 table
        # Lambda baryons
        if (self.pdgid.is_baryon
            and _digit(self.pdgid, Location.Nq2) == 1 and self.I == '0'  # 1st check alone is not sufficient to filter out lowest-ground Sigma's
            and self.pdgid.has_strange
            and not (self.pdgid.has_charm or self.pdgid.has_bottom or self.pdgid.has_top)
           ):
           return False
        if abs(self.pdgid) < 19: return False   # all quarks and neutrinos (charged leptons dealt with in 1st line of if statements ;-))
        if self.three_charge is None: return False  # deal with corner cases ;-)
        return True

    # Pretty descriptions

    def __str__(self):
        _tilde = '~' if self.anti_flag == Inv.Barred and self.pdgid < 0 else ''
        _charge = Charge_undo[self.three_charge] if self._charge_in_name() else ''
        return self.pdg_name + _tilde + _charge

    name = property(__str__, doc='The nice name, with charge added, and a tilde for an antiparticle, if relevant.')

    def _repr_latex_(self):
        name = self.latex_name
        # name += "^{" +  Parity_undo[self.three_charge] + '}'
        return ("$" + name + '$') if self.latex_name else '?'

    def _width_or_lifetime(self):
        """Display either the particle width or the lifetime.

        Internally used by the describe() method.
        """
        if self.width <= 0:
            return 'Width = {width} MeV'.format(width=str(self.width))
        elif self.width < 1.:  # corresponds to a lifetime of approximately 6.6e-22 seconds
            if self.width_lower == self.width_upper:
                e = width_to_lifetime(self.width-self.width_lower)-self.lifetime
                s = 'Lifetime = {lifetime} ns'.format(lifetime=str_with_unc(self.lifetime,e,e))
            else:
                s = 'Lifetime = {lifetime} ns'.\
                    format(lifetime=str_with_unc(self.lifetime,\
                                                 width_to_lifetime(self.width-self.width_lower)-self.lifetime,
                                                 self.lifetime-width_to_lifetime(self.width+self.width_upper)
                                                 ))
            return s
        else:
            return 'Width = {width} MeV'.format(width=str_with_unc(self.width, self.width_upper, self.width_lower))

    def describe(self):
        'Make a nice high-density string for a particle\'s properties.'
        if self.pdgid == 0:
            return "Name: Unknown"

        val = """Name: {self!s:<14} ID: {self.pdgid:<12} Latex: {latex_name}
Mass  = {mass} MeV
{width_or_lifetime}
Q (charge)        = {Q:<6}  J (total angular) = {self.J!s:<7}  P (space parity) = {P}
C (charge parity) = {C:<6}  I (isospin)       = {self.I!s:<7}  G (G-parity)     = {G}
""".format(self=self,
           G=Parity_undo[self.G],
           C=Parity_undo[self.C],
           Q=Charge_undo[self.three_charge],
           P=Parity_undo[self.P],
           mass=str_with_unc(self.mass, self.mass_upper, self.mass_lower),
           width_or_lifetime=self._width_or_lifetime(),
           latex_name = self._repr_latex_())

        if self.spin_type != SpinType.Unknown:
            val += "    SpinType: {self.spin_type!s}\n".format(self=self)
        if self.quarks:
            val += "    Quarks: {self.quarks}\n".format(self=self)
        val += "    Antiparticle name: {iself.name} (antiparticle status: {self.anti_flag.name})".format(iself=self.invert(), self=self)
        return val

    @property
    def programmatic_name(self):
        'This name could be used for a variable name.'
        return programmatic_name(self.name)

    @property
    def html_name(self):
        'This is the name using HTML instead of LaTeX.'
        return latex_to_html_name(self.latex_name)

    @classmethod
    def empty(cls):
        'Make a new empty particle.'
        return cls(0, 'Unknown', 0., 0., 0, Inv.Same)

    @classmethod
    def from_pdgid(cls, value):
        """
        Get a particle from a PDGID. Uses PDG data table.

        An exception is thrown if the input PDGID is invalid or if no matching PDGID is found.
        """
        if not is_valid(value):
            raise InvalidParticle("Input PDGID {0} is invalid!".format(value))
        table = cls.table()
        try:
            return table[table.index(value)]
        except ValueError:
            raise ParticleNotFound('Could not find PDGID {0}'.format(value))


    @classmethod
    def findall(cls, filter_fn=None, particle=None, **search_terms):
        '''
        Search for a particle, returning a list of candidates.

        The first and only positional argument is given each particle
        candidate, and returns True/False. Example:

            >>> Particle.findall(lambda p: 'p' in p.name)
            # Returns list of all particles with p somewhere in name

        You can pass particle=True/False to force a particle or antiparticle.
        If this is not callable, it will do a "fuzzy" search on the name. So this is identical:

            >>> Particle.findall('p')
            # Returns list of all particles with p somewhere in name

        You can also pass keyword arguments, which are either called with the
        matching property if they are callable, or are compared if they are not.
        This would do an exact search on the name, instead of a fuzzy search:

           >>> Particle.findall(name='p')
           # Returns proton and antiproton only

           >>> Particle.findall(name='p', particle=True)
           # Returns proton only

        Versatile searches require a (lambda) function as argument:

        >>> # Get all neutral beauty hadrons
        >>> Particle.findall(lambda p: p.pdgid.has_bottom and p.charge==0)
        >>>
        >>> # Trivially find all pseudoscalar charm mesons
        >>> Particle.findall(lambda p: p.pdgid.is_meson and p.pdgid.has_charm and p.spin_type==SpinType.PseudoScalar)

        See also ``find``, which throws an exception if the particle is not found or too many are found.
        '''

        # Note that particle can be called by position to keep compatibility with Python 2, but that behavior should
        # not be used and will be removed when support for Python 2.7 is dropped.

        # Remove any None values (makes programmatic access easier)
        for term in list(search_terms):
            if search_terms[term] is None:
                del search_terms[term]

        results = set()

        # Filter out values
        for item in cls.table():
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
                    except:
                        continue
                else:
                    if not(filter_fn in item.name):
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
                    if not value(pvalue):
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
        '''
        Require that your search returns one and only one result.
        The method otherwise raises a ParticleNotFound or RuntimeError exception.

        See findall for full listing of parameters.
        '''

        results = cls.findall(*args, **search_terms)

        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            raise ParticleNotFound('Did not find particle matching query: {}'.format(search_terms))
        else:
            raise RuntimeError("Found too many particles")

    @classmethod
    def from_dec(cls, name):
        'Get a particle from a .dec decay file (DecFile) style name - returns the best match.'

        # Catch 2 really special cases - names too short for a proper matching
        specials = {
            'n0': 'n',
            'anti-n0': 'n~',
            'p+': 'p',
            'anti-p-' : 'p~'
        }
        if name in specials:
            return cls.find(name=specials[name])

        # Extra special cases where the lowest-level particle
        # does *not* have the smallest PDG ID, which the query matches by default to.
        name = re.sub(r'Delta(?=[0\+\-][+-]?)', r'Delta(1232)', name)

        # Simplest search first - search by name
        try:
            return cls.find(name=name)
        except:
            pass

        # Many names defined in .dec files just aren't well-enough defined, hence are ambiguous!
        # Others are difficult to match with the standard regex rules.
        # The required mapping is here provided:
        dec_to_pdg_mapping = {
            "f_0": 'f(0)(980)',
            "f'_0": 'f(0)(1370)',
            "f'_1": 'f(1)(1420)',
            "h'_1": 'h(1)(1380)',
            'omega(2S)': 'omega(1420)',
            'phi' : 'phi(1020)',
            'K_L0': 'K(L)0',
            'K_S0': 'K(S)0',
            'B_s10': 'B(s1)(5830)0',
            "anti-D'_10": 'D(1)(2420)~0',
            'anti-B_s10': 'B(s1)(5830)~0',
            'J/psi': 'J/psi(1S)',
            'Upsilon': 'Upsilon(1S)',
            'Upsilon_2(1D)': 'Upsilon(2)(1D)',
            'Upsilon(5S)' : 'Upsilon(10860)',
            'X_1(3872)': 'X(3872)',
            'Omega_c*0': 'Omega(c)(2770)0',
            'Sigma_b+': 'Sigma(b)+',
            'Sigma_b*+': 'Sigma(b)*+',
        }
        if name in dec_to_pdg_mapping:
            return cls.find(name=dec_to_pdg_mapping[name])

        # In other cases a bulk replacement is more efficient given the several charge states possible.
        # Note: the dictionary needs to be sorted in such a way that the replacements for
        #       names of the kind "anti-X" are always dealt with before those for names "X".
        dec_to_pdg_replacements = {
            'a_0': 'a(0)(980)',
            'rho(2S)': 'rho(1450)',
            'anti-Sigma*': 'Sigma(1385)~',
            'anti-Xi*': 'Xi(1530)~',
            'anti-Sigma_c*': 'Sigma(c)(2520)~',
            'anti-Xi_c*': 'Xi(c)(2645)~',
            'anti-B_1': 'B(1)(5721)~',
            'Sigma*': 'Sigma(1385)',
            'Xi*': 'Xi(1530)',
            'Sigma_c*': 'Sigma(c)(2520)',
            'Xi_c*': 'Xi(c)(2645)',
            "D'_1": 'D(1)(2420)',
            'B_1': 'B(1)(5721)',
        }
        for oldw, neww in sorted(dec_to_pdg_replacements.items(), reverse=True):
            if oldw in name:
                return cls.find(name=name.replace(oldw, neww))

        # Special case of certain quarkonium states of the kind X_qj,
        # where q and j are the quark family (c, b) and total spin, respectively.
        for w in ('chi_', 'eta_'):
            if w in name: name = re.sub(r'\_(.*?)\(', r'(\1)(', name)

        mat = getdec.match(name)

        if mat is None:

            # Deal with antiquarks
            particle = None
            if "anti-" in name:
                name = name.replace('anti-', '')
                particle = False
                return cls.find(pdg_name=name, particle=particle)

            return cls.find(name=name, particle=particle)

        mat = mat.groupdict()

        # TODO: a lot of this should rather be done in the regex `getdec` - this is temporary
        if mat['name'] in ('f', 'h', 'chi', 'eta', 'omega', 'nu'):
            mat['charge'] = '0'
        if mat['name'] in ('B', 'Lambda', 'Sigma', 'Omega', 'Xi'):
            if mat['family'] is not None:
                if mat['charge'] is None:
                    mat['charge'] = '0'
                    mat['family'] = mat['family'][:-1]
        if mat['family'] is not None and mat['family'][-2:]=='10':
            mat['family'] = mat['family'][:-1]
            mat['charge'] = '0'
        if mat['state'] is not None and (mat['state']=='00' or mat['state']=='10' or mat['state']=='20'):
            mat['state'] = mat['state'][:-1]
            mat['charge'] = '0'

        try:
            return cls._from_group_dict_list(mat)[0]
        except IndexError:
            raise ParticleNotFound('{0} not found from dec-style name'.format(name))

    @classmethod
    def from_string(cls, name):
        'Get a particle from a PDG style name - returns the best match.'
        matches =  cls.from_string_list(name)
        if matches:
            return matches[0]
        else:
            raise ParticleNotFound('{0} not found in particle table'.format(name))

    @classmethod
    def from_string_list(cls, name):
        'Get a list of particles from a PDG style name.'

        # Forcible override
        particle = None

        short_name = name
        if '~' in name:
            short_name = name.replace('~','')
            particle = False

        mat = getname.match(short_name)
        if mat is None:
            list_can = cls.findall(name=name, particle=particle)
            if list_can:
                return list_can
            # If you don't have any matches there, try a fuzzier search that will capture antiparticles too
            else:
                return cls.findall(pdg_name=short_name, particle=particle)
        mat = mat.groupdict()

        if particle is False:
            mat['bar'] = 'bar'

        try:
            return cls._from_group_dict_list(mat)
        except ParticleNotFound:
            return []

    @classmethod
    def _from_group_dict_list(cls, mat):

        kw = dict()
        kw['particle'] = False if mat['bar'] is not None else (True if mat['charge'] == '0' else None)

        name = mat['name']

        if mat['family']:
            if '_' in mat['family']:
                mat['family'] = mat['family'].strip('_')
            name += '({mat[family]})'.format(mat=mat)
        if mat['state']:
            name += '({mat[state]})'.format(mat=mat)

        if 'prime' in mat and mat['prime']:
            name += "'"

        if mat['star']:
            name += '*'

        kw['J'] = float(mat['state']) if mat['state'] is not None else None

        if mat['mass']:
            maxname = name + '({mat[mass]})'.format(mat=mat)
        else:
            maxname = name

        if 'charge' in mat and mat['charge'] is not None:
            kw['three_charge'] = Charge_mapping[mat['charge']]

        vals = cls.findall(name = lambda x: maxname in x, **kw)
        if not vals:
            vals = cls.findall(name = lambda x: name in x, **kw)

        if not vals:
            raise ParticleNotFound("Could not find particle {0} or {1}".format(maxname, name))

        if len(vals) > 1 and mat['mass'] is not None:
            vals = [val for val in vals if mat['mass'] in val.latex_name]

        if len(vals) > 1:
            vals = sorted(vals)

        return vals
