# -*- encoding: utf-8 -*-

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
from .regex import getname, getdec

from .enums import (SpinType, Parity, Charge, Inv, Status,
                    Parity_undo, Parity_prog,
                    Charge_undo, Charge_prog, Charge_mapping)

from .utilities import programmatic_name, str_with_unc
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


    """
    pdgid = attr.ib(converter=PDGID)
    name = attr.ib()
    mass = attr.ib()
    width = attr.ib()
    anti = attr.ib(converter=Inv)  # Info about particle name for anti-particles

    rank = attr.ib(0)  # Next line is Isospin
    I = attr.ib(None)  # noqa: E741
    # J = attr.ib(None)  # Total angular momentum
    G = attr.ib(Parity.u, converter=Parity)  # Parity: '', +, -, or ?
    P = attr.ib(Parity.u, converter=Parity)  # Space parity
    C = attr.ib(Parity.u, converter=Parity)  # Charge conjugation parity
    # (B (just charge), F (add bar) , and '' (No change))
    quarks = attr.ib('', converter=str)
    status = attr.ib(Status.Nonexistent, converter=Status)
    latex = attr.ib('')
    mass_upper = attr.ib(0.0)
    mass_lower = attr.ib(0.0)
    width_upper = attr.ib(0.0)
    width_lower = attr.ib(0.0)

    def __repr__(self):
        return "<{self.__class__.__name__}: pdgid={pdgid}, fullname='{self!s}', mass={mass} MeV>".format(
            self=self, pdgid=int(self.pdgid),
            mass=str_with_unc(self.mass, self.mass_upper, self.mass_lower))
    _table = None # Loaded table of entries

    @classmethod
    def table(cls):
        """
        This accesses the internal particle data CSV table, loading it from the default location if needed.
        """
        if cls._table is None:
            cls.load_table()

        return cls._table

    @classmethod
    def load_table(cls, filename=None, append=False):
        """
        Load a particle data CSV table. Optionally append to the existing data already loaded if append=True.
        """
        if not append or cls._table is None:
            cls._table = []

        file_to_open = data.open_text(data, 'particle2018.csv') if filename is None else open(filename)

        with file_to_open as f:
            r = csv.DictReader(f)

            for v in r:
                value = int(v['ID'])
                name = v['Name']

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
                    anti=int(v['Anti']),
                    rank=int(v['Rank']),
                    status=int(v['Status']),
                    name=v['Name'],
                    quarks=v['Quarks'],
                    latex=v['Latex']))

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
       return self.three_charge / 3

    @property
    def three_charge(self):
        'The particle charge (integer * 3).'
        return Charge(self.pdgid.three_charge)

    @property
    def lifetime(self):
        'The particle lifetime, in nanoseconds.'
        return width_to_lifetime(self.width)

    @property
    def ctau(self):
        'The particle c*tau, in millimeters.'
        return c_light*self.lifetime

    @property
    def radius(self):
        'Particle radius, hard coded from the PDG data.'
        if abs(self.pdgid) in [411, 421, 431]:
            return 5.0
        else:
            return 1.5

    @property
    def bar(self):
        'Check to see if particle is inverted.'
        return self.pdgid < 0 and self.anti == Inv.Full

    @property
    def spin_type(self):  # -> SpinType:
        'Access the SpinType enum.'
        if self.J in [0, 1, 2]:
            J = int(self.J)

            if self.P == Parity.p:
                return (SpinType.Scalar, SpinType.Axial, SpinType.Tensor)[J]
            elif self.P == Parity.m:
                return (SpinType.PseudoScalar, SpinType.Vector, SpinType.PseudoTensor)[J]

        return SpinType.Unknown

    def invert(self):
        "Get the antiparticle."
        if self.anti == Inv.Full or (self.anti == Inv.Barless and self.three_charge != Charge.o):
            return self.from_pdgid(-self.pdgid)
        else:
            return copy(self)

    __neg__ = invert
    __invert__ = invert

    def _charge_in_name(self):
        if self.anti == Inv.Barless: return True
        if self.pdgid in (111, 130, 310): return True
        if self.three_charge == 0 and self.anti == Inv.Same: return False  # all quarkonia and the photon
        if self.pdgid.is_baryon and self.pdgid.has_strange \
           and not (self.pdgid.has_charm or self.pdgid.has_bottom): return False   # Lambda baryons
        if abs(self.pdgid) < 9: return False
        return True

    # Pretty descriptions

    def __str__(self):
        _tilde = '~' if self.anti == Inv.Full and self.pdgid < 0 else ''
        _charge = Charge_undo[self.three_charge] if self._charge_in_name() else ''
        return self.name + _tilde + _charge

    fullname = property(__str__, doc='The nice name, with charge added, and a tilde for an antiparticle, if relevant.')

    def _repr_latex_(self):
        name = self.latex
        # name += "^{" +  Parity_undo[self.three_charge] + '}'
        return ("$" + name + '$') if self.latex else '?'

    def _width_or_lifetime(self):
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

        val = """Name: {self.name:<10} ID: {self.pdgid:<12} Fullname: {self!s:<14} Latex: {latex}
Mass  = {mass} MeV
{width_or_lifetime}
I (isospin)       = {self.I!s:<6} G (parity)        = {G:<5}  Q (charge)       = {Q}
J (total angular) = {self.J!s:<6} C (charge parity) = {C:<5}  P (space parity) = {P}
""".format(self=self,
           G=Parity_undo[self.G],
           C=Parity_undo[self.C],
           Q=Charge_undo[self.three_charge],
           P=Parity_undo[self.P],
           mass=str_with_unc(self.mass, self.mass_upper, self.mass_lower),
           width_or_lifetime=self._width_or_lifetime(),
           latex = self._repr_latex_())

        if self.spin_type != SpinType.Unknown:
            val += "    SpinType: {self.spin_type!s}\n".format(self=self)
        if self.quarks:
            val += "    Quarks: {self.quarks}\n".format(self=self)
        val += "    Antiparticle status: {self.anti.name} (antiparticle name: {iself.fullname})".format(self=self, iself=self.invert())
        # val += "    Radius: {self.radius} GeV".format(self=self)
        return val

    @property
    def programmatic_name(self):
        'This name could be used for a variable name.'
        return programmatic_name(self.fullname)

    @property
    def html_name(self):
        'This is the name using HTML instead of LaTeX.'
        name = self.latex
        name = re.sub(r'\^\{(.*?)\}', r'<SUP>\1</SUP>', name)
        name = re.sub(r'\_\{(.*?)\}', r'<SUB>\1</SUB>', name)
        name = re.sub(r'\\mathrm\{(.*?)\}', r'\1', name)
        name = re.sub(r'\\left\[(.*?)\\right\]', r'[\1] ', name)
        name = name.replace(r'\pi', 'π').replace(r'\rho', 'ρ').replace(r'\omega', 'ω')
        name = re.sub(r'\\bar\{(.*?)\}', r'~\1', name)
        return name

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
    def from_search_list(cls, filter_fn=None, particle=None, **search_terms):
        '''
        Search for a particle, returning a list of candidates.

        The first and only positional argument is given each particle
        candidate, and returns true/false. Example:

            >>> Particle.from_search_list(lambda p: 'p' in p.fullname)
            # Returns list of all particles with p somewhere in fullname

        You can also pass particle=True/False to force a particle or antiparticle. If
        this is not callable, it will do a "fuzzy" search on the fullname. So this is identical:

            >>> Particle.from_search_list('p')
            # Returns list of all particles with p somewhere in name

        You can also pass keyword arguments, which are either called with the
        matching property if they are callable, or are compared if they are not.
        This would do an exact search on the name, instead of a fuzzy search:

           >>> Particle.from_search_list(name='p')
           # Returns proton and antiproton only

           >>> Particle.from_search_list(name='p', particle=True)
           # Returns proton only

        See also from_search, which throws an exception if the particle is not found or too many are found.
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
                    if not filter_fn(item):
                        continue
                else:
                    if not(filter_fn in item.fullname):
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
    def from_search(cls, *args, **search_terms):
        '''
        Require that your search returns one and only one result.
        The method otherwise raises a ParticleNotFound or RuntimeError exception.

        See from_search_list for full listing of parameters.
        '''

        results = cls.from_search_list(*args, **search_terms)

        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            raise ParticleNotFound('Did not find particle matching query: {}'.format(search_terms))
        else:
            raise RuntimeError("Found too many particles")

    @classmethod
    def from_dec(cls, name):
        'Get a particle from a DecFile style name - returns best match'

        mat = getdec.match(name)
        if mat is None:
            return cls.from_search(name=name)
        mat = mat.groupdict()

        return cls._from_group_dict_list(mat)[0]

    @classmethod
    def from_string(cls, name):
        'Get a particle from a PDG style name - returns best match'
        matches =  cls.from_string_list(name)
        if matches:
            return matches[0]
        else:
            raise ParticleNotFound('{0} not found in particle table'.format(name))



    @classmethod
    def from_string_list(cls, name):
        'Get a list of particle from a PDG style name'

        # Patch in common names
        if name == 'Upsilon':
            name = 'Upsilon(1S)'

        # Forcable override
        bar = False

        if '~' in name:
            name = name.replace('~','')
            bar = True

        mat = getname.match(name)
        if mat is None:
            return cls.from_search_list(name=name, particle=False if bar else None)
        mat = mat.groupdict()

        if bar:
            mat['bar'] = 'bar'

        try:
            return cls._from_group_dict_list(mat)
        except ParticleNotFound:
            return []

    @classmethod
    def _from_group_dict_list(cls, mat):

        #if '_' in mat['name']:
        #    mat['name'], mat['family'] = mat['name'].split('_')

        particle = False if mat['bar'] is not None else (True if mat['charge'] == '0' else None)

        fullname = mat['name']

        if mat['family']:
            fullname += '({mat[family]})'.format(mat=mat)
        if mat['state']:
            fullname += '({mat[state]})'.format(mat=mat)

        if mat['star']:
            fullname += '*'

        J = float(mat['state']) if mat['state'] is not None else None

        if mat['mass']:
            maxname = fullname + '({mat[mass]})'.format(mat=mat)
        else:
            maxname = fullname

        vals = cls.from_search_list(name = lambda x: maxname in x,
                                    three_charge=Charge_mapping[mat['charge']],
                                    particle=particle,
                                    J=J)
        if not vals:
            vals = cls.from_search_list(name = lambda x: fullname in x,
                                        three_charge=Charge_mapping[mat['charge']],
                                        particle=particle,
                                        J=J)

        if not vals:
            raise ParticleNotFound("Could not find particle {0} or {1}".format(maxname, fullname))

        if len(vals) > 1 and mat['mass'] is not None:
            vals = [val for val in vals if mat['mass'] in val.latex]

        if len(vals) > 1:
            vals = sorted(vals)

        return vals
