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

For convenience, all properties of the `PDGID` class are available as standalone functions:

.. code-block:: python

  >>> from particle.pdgid import is_meson
  >>>
  >>> is_meson(211)
  True

You can quickly display info from the command line with:

.. code-block:: bash

    python -m particle pdgid 311

Getting started: Particles
--------------------------

You can use a variety of methods to get particles; if you know the PDG number you can get a particle directly, or you
can use a search:

.. code-block:: python

    >>> Particle.from_pdgid(211)
    >>> Particle.from_search_list('pi')[0]

You can search for the properties using keyword arguments, which are `name`, `mass`, `width`, `charge`, `anti`, `rank`,
`I`, `J`, `G`, `P`, `quarks`, `status`, `latex`, `mass_upper`, `mass_lower`, `width_upper`, and `width_lower` (some of
those don\'t make sense). You can also use `.from_search()` to require only one match. You can also use the first two
arguments, called `name_s` and `latex_s` to do a loose search, and `name_re` and `latex_re` to do a regular expression
search.

Once you have a particle, any of the properties can be accessed, along with several methods. Though they are not real
properties, you can access `bar`, `radius`, and `spin_type`. You can also `invert()` a particle. There are lots of
printing choices, `describe()`, `programmatic_name()`, `html_name()`, html printing outs in notebooks, and of course
`repr` and `str` support.

You can quickly search for particles from the command line with:

.. code-block:: bash

    python -m particle search 311


You can put one or more PDG ID numbers here, or string names.

