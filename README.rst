particle: the pythonic version of HepPID and HepPDT
===================================================

.. image:: https://dev.azure.com/scikit-hep/particle/_apis/build/status/scikit-hep.particle?branchName=master
  :alt: Build Status
  :target: https://dev.azure.com/scikit-hep/particle/_build/latest?definitionId=1?branchName=master


particle provides a pythonic interface for the utility functions defined in HepPID and HepPDT,
see http://lcgapp.cern.ch/project/simu/HepPDT/.
These two packages give access to the Particle Data Group (PDG) particle data tables and particle identification codes.

The current version of the package reflects HepPDT and HepPID versions 3.04.01.

Installation
------------

Install ``particle`` like any other Python package:

.. code-block:: bash

    pip install particle

or similar (use ``--user``, ``virtualenv``, etc. if you wish).

Strict dependencies
-------------------

- `Python <http://docs.python-guide.org/en/latest/starting/installation/>`__ (2.7+, 3.4+)
- `importlib_resources backport <http://importlib-resources.readthedocs.io/en/latest/>`_ if using Python < 3.7
- `attrs <http://www.attrs.org/en/stable/>`_ provides classes without boilerplate (similar to DataClasses in Python 3.7)

Getting started: PDGIDs
-----------------------

.. code-block:: python

    >>> from particle.pdgid import PDGID
    >>>
    >>> pid = PDGID(211)
    >>> pid
    <PDGID: 211>
    >>> pid.is_meson
    True
    >>> pid = PDGID(99999999)
    >>> pid
    <PDGID: 99999999 (is_valid==False)>

For convenience, all properties of the ```PDGID`` class are available as standalone functions:

.. code-block:: python

    >>> from particle.pdgid import is_meson
    >>>
    >>> is_meson(211)
    True

PDGID literals provide (``PDGID`` class) aliases for the most common particles, with easily recognisable names.
For example:

.. code-block:: python

    >>> from particle.pdgid import literals as lid
    >>>
    >>> lid.pi_plus
    <PDGID: 211>
    >>>
    >>> from particle.pdgid.literals import Lb0
    >>>> Lb0
    <PDGID: 5122>
    >>> Lb0.has_bottom
    True

You can quickly display PDGID info from the command line with:

.. code-block:: bash

    $ python -m particle pdgid 323
    <PDGID: 323>
    A              None
    J              1.0
    L              0
    S              1
    Z              None
    abspid         323
    charge         1.0
    has_bottom     False
    ...

Getting started: Particles
--------------------------

You can use a variety of methods to get particles. If you know the PDGID number you can get a particle directly, or you
can use a search:

.. code-block:: python

    >>> from particle import Particle
    >>> Particle.from_pdgid(211)
    <Particle: pdgid=211, fullname='pi+', mass=139.57061 ± 0.00024 MeV>
    >>>
    >>> Particle.from_search_list('pi')[0]
    <Particle: pdgid=111, fullname='pi0', mass=134.9770 ± 0.0005 MeV>

You can search for the properties using keyword arguments, which are
``name``, ``mass``, ``width``, ``charge``, ``anti``, ``rank``,
``I``, ``J``, ``G``, ``P``, ``quarks``, ``status``, ``latex``,
``mass_upper``, ``mass_lower``, ``width_upper``, and ``width_lower``
(some of those don\'t make sense).
The alternative ``.from_search()`` requires only one match returned by the search.
You can also use the first two arguments, called ``name_s`` and ``latex_s``
to do a loose search, and ``name_re`` and ``latex_re`` to do a regular expression search.

Once you have a particle, any of the properties can be accessed, along with several methods.
Though they are not real properties, you can access ``bar``, ``radius``, and ``spin_type``.
You can also ``.invert()`` a particle.

There are lots of printing choices for particles:
``describe()``, ``programmatic_name``, ``html_name``, HTML printing outs in notebooks,
and of course ``repr`` and ``str`` support.

You can get the ``.pdgid`` from a particle, as well.
Sorting particles will put lowest abs(PDGID) first.


Particle literals provide (``Particle`` class) aliases for the most common particles,
with easily recognisable names. For example:

.. code-block:: python

    >>> from particle.particle import literals as lp
    >>> lp.pi_plus
    <Particle: pdgid=211, fullname='pi+', mass=139.57061 ± 0.00024 MeV>
    >>>
    >>> from particle.particle.literals import Lb0
    >>>> Lb0
    <Particle: pdgid=5122, fullname='Lambda(b)0', mass=5619.60 ± 0.17 MeV>
    >>> Lb0.J
    0.5

You can quickly search for particles from the command line with:

.. code-block:: bash

    $ python -m particle search 'K*0'
    <Particle: pdgid=313, fullname='K*(892)0', mass=895.55 +/- 0.20 MeV>
    <Particle: pdgid=30313, fullname='K*(1680)0', mass=1718 +/- 18 MeV>
    <Particle: pdgid=100313, fullname='K*(1410)0', mass=1421 +/- 9 MeV>

If you only select one particle, either by a search or by giving the PDGID number, you can see more information about
the particle:

.. code-block:: bash

    $ python -m particle search 311
    Name: K          ID: 311          Fullname: K0             Latex: $K^{0}$
    Mass  = 497.611 ± 0.013 MeV
    Width = -1.0 MeV
    I (isospin)       = 1/2    G (parity)        = 0      Q (charge)       = 0
    J (total angular) = 0.0    C (charge parity) = 0      P (space parity) = ?
        Quarks: dS
        Antiparticle status: Full (antiparticle name: K~0)
