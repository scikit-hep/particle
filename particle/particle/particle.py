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

from .. import data
from ..pdgid import PDGID
from .regex import getname, getdec

from .enums import (SpinType, Par, Charge, Inv, Status,
                    Par_undo, Par_prog)

from .utilities import programmatic_name, mkul, str_with_unc

class ParticleNotFound(RuntimeError):
    pass


@total_ordering
@attr.s(slots=True, cmp=False, repr=False)
class Particle(object):
    'The Particle object class. Hold a series of properties for a particle.'
    val = attr.ib(converter=PDGID)
    name = attr.ib()
    mass = attr.ib()
    width = attr.ib()
    anti = attr.ib(converter=Inv)  # Info about particle name for anti-particles

    rank = attr.ib(0)  # Next line is Isospin
    I = attr.ib(None)  # noqa: E741
    # J = attr.ib(None)  # Total angular momentum
    G = attr.ib(Par.u, converter=Par)  # Parity: '', +, -, or ?
    P = attr.ib(Par.u, converter=Par)  # Space parity
    C = attr.ib(Par.u, converter=Par)  # Charge conjugation parity
    # (B (just charge), F (add bar) , and '' (No change))
    quarks = attr.ib('', converter=str)
    status = attr.ib(Status.Nonexistant, converter=Status)
    latex = attr.ib('')
    mass_upper = attr.ib(0.0)
    mass_lower = attr.ib(0.0)
    width_upper = attr.ib(0.0)
    width_lower = attr.ib(0.0)

    def __repr__(self):
        return "<{self.__class__.__name__}: val={val}>, name='{self.name}', mass={mass} MeV>".format(
            self=self, val=int(self.val),
            mass=str_with_unc(self.mass, self.mass_upper, self.mass_lower))
    _table = None # Loaded table of entries

    @classmethod
    def table(cls):
        if cls._table is None:
            cls.load_table()

        return cls._table

    @classmethod
    def load_table(cls, filename=None, append=False):
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
                    val=value,
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
            return self.val == other.val
        except AttributeError:
            return self.val == other

    # Only one particle can exist per PDGID number
    def __hash__(self):
        return hash(self.val)


    # Integer == PDGID
    def __int__(self):
        return int(self.val)

    @property
    def J(self):
        'The J quantum number'
        return self.val.J

    @property
    def charge(self):
        'The particle charge'
        return Charge(self.val.charge)

    @property
    def radius(self):
        'Particle radius, hard coded'
        if abs(self.val) in [411, 421, 431]:
            return 5.0
        else:
            return 1.5

    @property
    def bar(self):
        'Check to see if particle is inverted'
        return self.val < 0 and self.anti == Inv.Full

    @property
    def spin_type(self):  # -> SpinType:
        'Access the SpinType enum'
        if self.J in [0, 1, 2]:
            J = int(self.J)

            if self.P == Par.p:
                return (SpinType.Scalar, SpinType.Axial, SpinType.Tensor)[J]
            elif self.P == Par.m:
                return (SpinType.PseudoScalar, SpinType.Vector, SpinType.PseudoTensor)[J]

        return SpinType.Unknown

    def invert(self):
        "Get the antiparticle"
        if self.anti == Inv.Full or (self.anti == Inv.Barless and self.charge != Par.o):
            return self.from_pdgid(-self.val)
        else:
            return copy(self)

    __neg__ = invert
    __invert__ = invert

    # Pretty descriptions

    def __str__(self):
        tilde = '~' if self.anti == Inv.Full and self.val < 0 else ''
        # star = '*' if self.J == 1 else ''
        return self.name + tilde + Par_undo[self.charge]

    def _repr_latex_(self):
        name = self.latex
        if self.bar:
            name = re.sub(r'^(\\mathrm{|)([\w\\]\w*)', r'\1\\bar{\2}', name)
        return ("$" + name + '$') if self.latex else '?'

    def describe(self):
        'Make a nice high-density string for a particle\'s properties.'
        if self.val == 0:
            return "Name: Unknown"

        val = """Name: {self.name:<10} ID: {self.val:<12} Fullname: {self!s:<14} Latex: {latex}
Mass  = {self.mass:<10.9g} {mass} MeV
Width = {self.width:<10.9g} {width} MeV
I (isospin)       = {self.I!s:<6} G (parity)        = {G:<5}  Q (charge)       = {Q}
J (total angular) = {self.J!s:<6} C (charge parity) = {C:<5}  P (space parity) = {P}
""".format(self=self,
           G=Par_undo[self.G],
           C=Par_undo[self.C],
           Q=Par_undo[self.charge],
           P=Par_undo[self.P],
           mass=mkul(self.mass_upper, self.mass_lower),
           width=mkul(self.width_upper, self.width_lower),
           latex = self._repr_latex_())

        if self.spin_type != SpinType.Unknown:
            val += "    SpinType: {self.spin_type!s}\n".format(self=self)
        if self.quarks:
            val += "    Quarks: {self.quarks}\n".format(self=self)
        val += "    Antiparticle status: {self.anti.name}\n".format(self=self)
        val += "    Radius: {self.radius} GeV".format(self=self)
        return val

    @property
    def programmatic_name(self):
        'This name could be used for a variable name'
        name = self.name
        name += '_' + Par_prog[self.charge]
        return programmatic_name(name)

    @property
    def html_name(self):
        'This is the name using HTML instead of LaTeX'
        name = self.latex
        name = re.sub(r'\^\{(.*?)\}', r'<SUP>\1</SUP>', name)
        name = re.sub(r'\_\{(.*?)\}', r'<SUB>\1</SUB>', name)
        name = re.sub(r'\\mathrm\{(.*?)\}', r'\1', name)
        name = re.sub(r'\\left\[(.*?)\\right\]', r'[\1] ', name)
        name = name.replace(r'\pi', 'π').replace(r'\rho', 'ρ').replace(r'\omega', 'ω')
        if self.bar:
            name += '~'
        return name

    @classmethod
    def empty(cls):
        'Get a new empty particle'
        return cls(0, 'Unknown', 0., 0., 0, Inv.Same)

    @classmethod
    def from_pdgid(cls, value):
        'Get a particle from a PDGID. Uses PDG data table.'
        table = cls.table()
        return table[table.index(value)]


    @classmethod
    def from_search_list(cls, name_s=None, latex_s=None, name_re=None, latex_re=None, particle=None, **search_terms):
        '''
        Search for a particle, returning a list of candidates

        Terms are:
           name_s: A loose match (extra terms allowed) for Name
           name_re: A regular expression for Name
           latex_s: A loose match (extra terms allowed) for Latex
           latex_re: A regular expression for Latex
           particle: True/False, for particle/antiparticle

           Any other attribute: exact match for attribute value

        This method returns a list; also see from_search, which throws an error if the particle is not found or too many found.
        '''

        for term in list(search_terms):
            if search_terms[term] is None:
                del search_terms[term]

        # Special case if nothing was passed
        if (not search_terms
            and particle is None
            and name_s is None
            and name_re is None
            and latex_s is None
            and latex_re is None):

            return []

        # If I is passed, make sure it is a string
        if not isinstance(search_terms.get('I', ''), str):
            search_terms['I'] = str(search_terms['I'])

        results = set()

        # Filter out values
        for item in cls.table():
            if particle is not None:
                if particle and int(item) < 0:
                    continue
                elif (not particle) and int(item) > 0:
                    continue

            passing = True
            for term in search_terms:
                if getattr(item, term) != search_terms[term]:
                    passing = False

            if not passing:
                continue

            if name_s is not None:
                if name_s not in item.name:
                    continue

            if name_re is not None:
                if not re.search(name_re, item.name):
                    continue

            if latex_s is not None:
                if not latex_s in item.latex:
                    continue

            if latex_re is not None:
                if not re.search(latex_re, item.latex):
                    continue

            results.add(item)

        return sorted(results)

    @classmethod
    def from_search(cls, **search_terms):
        '''
        Require that your each returns one and only one result

        See from_search_list for full listing of parameters
        '''

        results = cls.from_search_list(**search_terms)

        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            raise ParticleNotFound('Did not find particle matching query: {}'.format(search_terms))
        else:
            raise RuntimeError("Found too many particles")

    @classmethod
    def from_dec(cls, name):
        'Get a particle from a DecFile style name'

        mat = getdec.match(name)
        if mat is None:
            return cls.from_search(name=name)
        mat = mat.groupdict()

        return cls._from_group_dict(mat)


    @classmethod
    def from_string(cls, name):
        'Get a particle from an AmpGen (PDG) style name'

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
            return cls.from_search(name=name, particle=False if bar else None)
        mat = mat.groupdict()

        if bar:
            mat['bar'] = 'bar'

        return cls._from_group_dict(mat)

    @classmethod
    def _from_group_dict(cls, mat):

        #if '_' in mat['name']:
        #    mat['name'], mat['family'] = mat['name'].split('_')

        Par_mapping = {'++': 2, '+': 1, '0': 0, '-': -1, '--': 2}
        particle = False if mat['bar'] is not None else (True if mat['charge'] == '0' else None)

        fullname = mat['name']
        if mat['family']:
            fullname += '({mat[family]})'.format(mat=mat)
        if mat['state']:
            fullname += '({mat[state]})'.format(mat=mat)

        if mat['star'] and not mat['state']:
            J = 1
        else:
            J = float(mat['state']) if mat['state'] is not None else None

        if mat['mass']:
            maxname = fullname + '({mat[mass]})'.format(mat=mat)
        else:
            maxname = fullname

        vals = cls.from_search_list(name=maxname,
                                    charge=Par_mapping[mat['charge']],
                                    particle=particle,
                                    J=J)
        if not vals:
            vals = cls.from_search_list(name=fullname,
                                        charge=Par_mapping[mat['charge']],
                                        particle=particle,
                                        J=J)

        if not vals:
            raise ParticleNotFound("Could not find particle {0} or {1}".format(maxname, fullname))

        if len(vals) > 1 and mat['mass'] is not None:
            vals = [val for val in vals if mat['mass'] in val.latex]

        if len(vals) > 1:
            vals = sorted(vals)

        return vals[0]

