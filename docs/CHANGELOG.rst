Changelog
=========

Version 0.10.0
--------------
In preparation.

* ``Particle`` class:
  - Several improvements, in particular to better deal with nuclei and diquarks.
  - Speed of table loading improved.
  - Particle enums extended for diquarks.
  - Make particle literals available from top-level import.
  - Print-outs made more consistent for missing and non-relevant particle properties.
  - New tests added.
* ``PDGID`` class:
  - PDG ID functions extended to correctly and consistently deal with nuclei.
* Data CSV files:
  - Version 5 of package data files, with
    - Diquarks added.
    - Information in nuclei added! List and masses taken from package ``periodictable`` version 1.5.2.
    - A couple of PDG ID numbers corrected (they had evolved in time).
  - Converter script adapted to add to the produced data files
    particles not in the PDG data table, such as diquarks.
* Redesigned packaging system.
* Miscellaneous:
  - Files ``*requirements.txt`` removed from package - use ``pip install .[dev]`` instead
  - Warning from ``collections.abc`` fixed, keeping compatibility with Python 2.
  - Deprecation warning in ``attr.s`` fixed,
    requirement on minimal version of ``attr`` added.


Version 0.9.2
-------------
February 14th, 2020

* ``Particle`` class:
  - Deal with particles with no mass info.
  - Make ``Particle.dump_table()`` work better in notebooks.


Version 0.9.1
-------------
January 14th, 2020

* ``Particle`` class:
  - Documentation added to various methods.
  - Minor fix to class method ``from_evtgen_name(...)``.


Version 0.9.0
-------------
January 7th, 2020

* ``Particle`` class:
  - Robust handling of missing mass info.
* Data CSV files:
  - Version 4 of package data files,
    with more particles added (mostly badly-known particles relevant for MC).
  - Version header now also present in the ``particleXXXX.csv`` files.


Version 0.8.1
-------------
December 14th, 2019

* Fix of lifetimes/widths (unknown) for corner cases.
* Documentation updates.


Version 0.8.0
-------------
December 3rd, 2019

* Changes in API:
  - ``GeantID`` class renamed to ``Geant3ID``.
* Data CSV files:
  - Version 3 (and 2) of package data files,
    which contain new entries and fixes for certain information in 2008 PDG extended data file.
  - File ``data/pdgid_to_geantid.csv`` renamed to ``data/pdgid_to_geant3id.csv``.
  - 2016 and 2017 PDG data files ``mass_width_2016.mcd`` and ``mass_width_2017.mcd`` removed.
* Tests:
  - Tests for ``converters`` submodule added.
  - Tests for ``Geant3ID`` extended.
* Miscellaneous:
  - Package files formatted with ``Black`` package.


Version 0.7.1
-------------
November 22nd, 2019

* ``Particle`` class:
  - Isospin property returns a float.
  - New property ``is_unflavoured_meson``.
  - More tests for P and C quantum numbers.
* ``PDGID`` class:
  - Non-robust P and C properties removed.
* Data CSV files:
  - Versioning introduced, see comment on first line of files.
  - File ``data/pdgid_to_evtgenname.csv`` extended with extra information.
  - More documentation.
* MC particle identification code converters:
  - Core ``BiMap`` class simplified.


Version 0.7.0
-------------
November 19th, 2019

* Enhancements to ``Particle`` class:
  - Dummy/unknown particle width and lifetime errors stored as ``None``.
  - More particle name and ``PDGID`` literals for b-baryons.
  - Fix for the ``D(s2)*(2573)`` LaTeX name.
  - ``InvalidParticle`` made available at top-level import.
* Changes in API:
  - ``Particle.from_dec...()`` renamed to ``Particle.from_evtgen_name(...)``.
* MC particle identification code converters:
  - Introduced directional maps ``PDG2EvtGenNameMap`` and ``EvtGen2PDGNameMap`` between PDG and EvtGen names.
  - Conversions master file ``data/conversions.csv`` added.
  - Content of converters CSV files are now ordered.
* Documentation:
  - README updated with new package functionality.
* Support for Python 3.4 removed and support for Python 3.8 added.


Version 0.6.2
-------------
September 19th, 2019

* Fix for inconsistent PDG ID and name of Upsilon_2(1D).
* Several fixes for renames of particle names by the PDG.


Version 0.6.1
-------------
September 6th, 2019

* Enhancement to ``Particle.dump_table()``.
* Added tests for Pythia and Geant identification code converters.
* Particle table CSV file updated for PDG change of 3 particle names.


Version 0.6.0
-------------
September 1st, 2019

* Introduction of classes for MC particle identification codes:
  - ``PythiaID`` class.
  - ``GeantID`` class.
* Introduction of MC particle identification code converters:
  - Generic ``BiMap`` bi-bidirectional map class.
  - ``Pythia2PDGIDBiMap`` bi-directional map between PDG and Pythia IDs.
  - ``Geant2PDGIDBiMap`` bi-directional map between PDG and Geant IDs.
  - ``EvtGenName2PDGIDBiMap`` bi-directional map between PDG IDs and EvtGen names.
* New data files:
  - File ``data/pdgid_to_pythiaid.csv`` for PDGID-PythiaID conversions.
  - File ``data/pdgid_to_geantid.csv`` for PDGID-GeantID conversions.
  - File ``data/pdgid_to_evtgenname.csv `` for PDG ID - EvtGen name conversions.


Version 0.5.2
-------------
August 26th, 2019

* Better handling of LaTeX to HTML conversions of particle names.
* Added the tabulate package dependency to the zipapp.


Version 0.5.1
-------------
August 21st, 2019

* Added ``Particle.dump_table(...)`` method.
* Added tests for default/dummy particle (PDG ID = mass = 0).
* Demo notebook updated.
* Doctests introduced in the CI.
* Dependency on package ``six`` removed.


Version 0.5.0
-------------
June 14th, 2019

* Added the 2019 PDG data table, now default.
  - Some poorly established particles not in the current PDG data files
    were previously erroneously made available. They have now been removed.
* Changes in API:
    - ``Particle.table()`` renamed to ``Particle.all()``.
* Enhancements to ``Particle`` class:
  - Numerous LaTeX particle names updated.
  - Correctly deal with experimental width upper limits.
  - Better display of lifetimes and widths.
  - More tests.
* Demo notebook added, with a launcher for Binder in the README.
* Extra tests for particle searches.


Version 0.4.4
-------------
May 13th, 2019

* Setup improvements.
* zipapp CI added.
* Particle search methods made robust against exceptions.


Version 0.4.3
-------------
May 10th, 2019

* Searches given a .dec decay file particle name:
  - Speed-up of searches.
  - Corner cases dealt with.
  - Extended test suite for the ``Particle.from_dec(...)`` method.
* Added Particle.is_self_conjugate property.
* Bug fix in the PDG extended file from 2008 (in excited K, D and B meson names).


Version 0.4.2
-------------
April 29th, 2019

* Added re-release of the 2018 PDG data table (neutrinos added, formatting fixes).
* CI scripts for Azure enhanced.
* Test coverage improvements.
* Wheel now available on PyPI.


Version 0.4.1
-------------
April 2th, 2019

* Enhancements to  ``Particle`` class:
  - Particles in .dec decay files dealt with, see ``Particle.from_dec(...)`` method.
  - Loading tables made nicer, with more documentation.
  - Particle charge is an entry of CSV files again, so that user particles are better dealt with.
* Bug fix for corner cases of using the package for non-valid particles.
* Work on documentation.
* PyPI badge created from https://img.shields.io.


Version 0.4.0
-------------
March 20th, 2019

* Changes in API:
    - Rename ``Particle.from_search/from_search_list`` to ``Particle.find/findall``.
    - Rename ``Particle.fullname/name`` to ``Particle.name/pdg_name``.
    - Rename ``Particle.bar`` to ``Particle.is_name_barred``.
    - Rename ``Particle.latex`` to ``Particle.latex_name``.
* Neutrinos added to the 2018 data files.
* Better print-out of particle properties.
* Better handling of particle names in HTML and LaTeX.
* Better handling of ``Particle.empty()``.
* Test suite of ``particle`` and ``pdgid`` submodules improved and extended.
* Comprehensive package documentation (data files, ``particle`` and ``pdgid`` submodules).
* Added utility conversion function of particle names from LaTeX to HTML.
* Fixed LaTeX names of Delta(1232) baryons in ``data\pdgid_to_latex.csv`` file.
* Several bug fixes.
* Simpler usage of ``particle.particle.convert`` (non-public helper module).


Version 0.3.0
-------------
March 6th, 2019

* ``Particle`` search engine replaced with more intuitive and powerful version.
* Various improvements in the handling of particle names and literals.
* List of literals extended.
* More documentation in ``Particle`` class.
* More tests; table generation is now tested as well.
* Bug fixes in CSV data files and LaTeX naming updates.
* Added missing particles for 2018 data files.


Version 0.2.2
-------------
Feb 5th, 2019

* Bug fix in ``setup.py``.
* CHANGELOG file added.


Version 0.2.1
-------------
Feb 4th, 2019

* ``Particle`` now has direct lifetime and ctau access.
* Better documentation.
* Several bugs fixed in ``Particle`` and ``PDGID``.
* The minimum version of dependencies are now more accurate.

The Scikit-HEP package ``hepunits`` is now a strict dependency.


Version 0.2.0
-------------
Jan 29, 2019

Particle provides a pythonic interface to the Particle Data Group (PDG)
particle data tables and particle identification codes.


Version 0.1.0
-------------
Dec 19, 2018

First release, Python version of HepPID.
