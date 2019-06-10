Changelog
=========

Version 0.5.0
-------------
In development.

* Changes in API:
    - ``Particle.table()`` renamed to ``Particle.all()``.
* Added the 2019 PDG data table, now default.
* Enhancements to  ``Particle`` class:
  - Numerous LaTeX particle names updated.
  - Better display of lifetimes and widths.
  - More tests.
* Demo notebook added, with a launcher for Binder.
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
