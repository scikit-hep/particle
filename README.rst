hepparticle: the pythonic version of HepPID and HepPDT
======================================================

hepparticle provides a pythonic interface for the utility functions defined in HepPID and HepPDT, see http://lcgapp.cern.ch/project/simu/HepPDT/.
These two packages give access to the Particle Data Group (PDG) particle data tables and particle identification codes.

The current version of the package reflects HepPDT and HepPID versions 3.04.01.

Installation
------------

Install ``hepparticle`` like any other Python package:

.. code-block:: bash

    pip install hepparticle

or similar (use ``--user``, ``virtualenv``, etc. if you wish).

Strict dependencies
-------------------

- `Python <http://docs.python-guide.org/en/latest/starting/installation/>`__ (2.7+, 3.4+)

Getting started
---------------

.. code-block:: python

   >>> from hepparticle import PDGID
   >>>
   >>> pid = PDGID(211)
   >>> pid
   <PDGID: 211>
   >>> pid.is_meson
   True
   >>> pid = PDGID(99999999)
   >>> pid
   <PDGID: 99999999(is_valid==False)>

For convenience, all properties of the `PDGID` class are available as standalone functions:

.. code-block:: python

  >>> from hepparticle import is_meson
  >>>
  >>> is_meson(211)
  True
