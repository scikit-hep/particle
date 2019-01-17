particle: the pythonic version of HepPID and HepPDT
===================================================

.. image:: https://dev.azure.com/scikit-hep/particle/_apis/build/status/scikit-hep.particle?branchName=master
  :alt: Build Status
  :target: https://dev.azure.com/scikit-hep/particle/_build/latest?definitionId=1?branchName=master
  

particle provides a pythonic interface for the utility functions defined in HepPID and HepPDT, see http://lcgapp.cern.ch/project/simu/HepPDT/.
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

Getting started
---------------

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
