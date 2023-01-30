Changelog
=========

Version 0.21.2
--------------

January 30th, 2023

- Classes for MC particle identification codes and converters:
  - Improvements and fixes in Corsika7 module.
  - Full test coverage for Corsika7 module.
  - Better test coverage for PDG ID related functions.
- Tests:
  - Updates to pre-commit hooks.


Version 0.21.1
--------------

January 4th, 2023

- `Particle` class and submodules:
  - Better test coverage.
- `PDGID` class method and related standalone functions:
  - Minor code simplifications.
  - Significant improvements to test coverage.
- Documentation:
  - README: info added on how to create user-defined particles.
- Tests:
  - Various improvements to the CI.
  - Updates to pre-commit hooks and CI YAML files.


Version 0.21.0
--------------

November 8th, 2022

- Data files:
  - Added the 2022 PDG data table file, now default.
  - Version 11 of package CSV data files:
      - Since PDG 2022 information now the default.
- Classes for MC particle identification codes and converters:
  - New `Corsika7ID` class.
  - New `Corsika72PDGIDBiMap` bi-directional map between PDG and Corsika7 IDs.
- `Particle` class, `PDGID` like classes and related standalone functions:
  - New method `Particle.from_nucleus()`.
  - Extra documentation.
- Miscellaneous:
  - Added a CITATION.cff file.
  - Moved over to using hatchling.
  - Added support for Python 3.11 and dropped support for Python 3.6.
  - Adapted to Pandas 1.5 series (removal of deprecation warnings).
- Documentation:
   - Minor README updates.
- Tests:
  - Updates to pre-commit hooks and CI YAML files.
  - Various improvements to the CI.


Version 0.20.1
--------------

March 29th, 2022

- `Particle` class:
  - More tests of PDGID functions for special particles.
- Experiment-specific modules:
  - `particle.lhcb` simplified.
- Miscellaneous:
  - Minor cleanup and updates.
- Tests:
  - Now included in the SDist (`MANIFEST.in` updated).
  - Pre-commit hooks updated.


Version 0.20.0
--------------

January 15th, 2022

**First Python 3 (3.6+) only version.**

- `Particle` class:
  - Deprecated method `find` method removed. Use `findall` or `finditer` instead.
  - HTML Greek letters in particle names use hex code rather than entity name.
- `PDGID` class method and related standalone functions:
  - Deprecated function `is_composite_quark_or_lepton` removed. Use `is_excited_quark_or_lepton` instead.
- Documentation:
  - README updated with info on the new experiment-specific module `particle.lhcb`.
- Miscellaneous:
  - Support for Python 2 and Python 3.5 dropped.
  - Full static typing implemented.
- Tests:
  - Pre-commit hooks updated.


Version 0.16.3
--------------

December 15th, 2021

- `Particle` class:
  - New class method `Particle.from_name`.
- New experiment-specific module:
  - Module `particle.lhcb` with functions and mappings to deal with particle names in use in LHCb software.
  - Script `admin/dump_pdgid_to_lhcb.py` to generate the PDGID <-> LHCb name mapping (CSV file).
- Tests:
  - Updated pre-commit hooks.


Version 0.16.2
--------------

November 11th, 2021

- `Particle` class:
  - Faster `Particle.from_pdgid`.
  - Better coverage of documentation for `Particle` methods, especially for newest method `finditer`.
  - Do not expose converters on high-level imports. Usage is hence `from particle.converters import ...`.
- Tests:
  - Resurrected tests on "all" platforms - Linux, macOS and Windows.
  - Performance benchmark tests added for loading of particle property CSV files.
  - Updated pre-commit hooks.
- Miscellaneous:
  - Enforced `Black` formatting in notebooks.


Version 0.16.1
--------------

September 10th, 2021

- Fixed an regression with the import time being unreasonably slow.
- Restore Python 3.5 support (no benefit to drop until 2.7 is dropped)


Version 0.16.0
--------------

September 1st, 2021

- `Particle` class:
  - Added `finditer`, which returns an iterator instead of a complete list like `findall`.
  - Method `find` deprecated. It will be removed from version 0.17.0 onwards.
    Please use the more general `findall` method, or the new `finditer` method.
- `PDGID` class:
  - New functions `is_sm_lepton`, `is_sm_quark` and `is_excited_quark_or_lepton`
    for qualification of PDG IDs.
  - `is_composite_quark_or_lepton` deprecated in favour of better named `is_excited_quark_or_lepton`.
  - `is_lepton` fixed to match the behaviour of the related `is_quark`,
     i.e. now excited leptons are not considered leptons (only SM and 4th generation leptons).
  - Improvements to documentation.
  - Test suite enhanced accordingly.
- Data files:
  - Added the 2021 PDG data table .mcd file, now default.
  - Version 10 of package CSV data files:
      - Since PDG 2021 information now the default.
  - Lifetimes of neutrinos set to infinity.
  - Check added for duplicate entries in .mcd PDG data files.
- Tests:
  - Tests of coverage added back, using Codecov on GHAs.
  - CI enhanced, e.g. adding codespell, isort and flake8 checks tp pre-commit hooks.
- Miscellaneous:
  - Support for Python 3.10 added.
  - Several `FutureWarning` warnings fixed.
  - Code modernisation.


Version 0.15.1
--------------

June 24th, 2021

- `Particle` class:
  - Bug fix in `Particle.to_dict`.
- Tests:
  - CI improvements.
  - Azure pipelines removed since superseded by GitHub Actions.
- Miscellaneous:
  - Code improvements thanks to Sourcery.
  - Clean-up of unnecessary files/code.


Version 0.15.0
--------------

May 18th, 2021

- `Particle` class:
  - Literals now defined for all particles in the loaded "database" CSV file, excluding nuclei.
  - Defined and/or fixed the programmatic names for diquarks and SUSY particles.
- Data CSV files:
  - Version 9 of package data files, with all antiparticle bars done with `\overline` instead of `\bar`.
- Miscellaneous:
  - Added `latex_name_unicode()` function to convert in particle names in LaTeX all greek letters by their unicode.
  - Added a `.zenodo.json` file to provide enhanced metadata for Zenodo.
  - CI updates for newer versions of Black and pre-commit.


Version 0.14.1
--------------

March 23rd, 2021

- Code refactored in the CI by Sourcery.ai.
- Updates to versions of pre-commit hooks.


Version 0.14.0
--------------

November 26th, 2020

- `Particle` class:
  - Methods `Particle.to_list` and `Particle.to_dict` enhanced.
- Data CSV files:
  - Version 8 of package data files, with fixed parities for antibaryons with undefined parity.
  - Tests added to check if every particle is parsed and loaded correctly.
- Miscellaneous:
  - Minor fix on static typing.


Version 0.13.1
--------------

November 10th, 2020

- PDG ID:
  - Minor simplifications in some PID functions.
- `Particle` class:
  - Test for `Particle.is_unflavoured_meson` added.
- Miscellaneous:
  - Full static typing implemented.


Version 0.13.0
--------------

October 30th, 2020

- Dependencies:
  - hepunits >= 2.0.0.
- Tests:
  - CI updates.
  - Tests adapted to hepunits 2.0.0.
- Miscellaneous:
  - Support for Python 3.9 added.


Version 0.12.0
--------------

September 29th, 2020

- `Particle` class:
  - `Particle.dump_table()` method removed and replaced with methods
    `Particle.to_dict()` and `Particle.to_list()` (avoids strong coupling of packages).
  - Improve LaTeX particle names with `\prime` in them,
    to have correct HTML names for such particles.
  - Misleading/awkward `Particle.__int__` method removed.
- `PDGID` class:
  - New functions for qualification of PDG IDs:
    - `is_quark`.
    - `is_gauge_boson_or_higgs`.
    - `is_sm_gauge_boson_or_higgs`.
    - `is_generator_specific`.
    - `is_technicolor`.
    - `is_composite_quark_or_lepton`.
    - `is_special_particle`.
  - Several PDG ID qualification functions improved and/or enhanced,
    and minor bugs fixed for certain special particles.
- Data CSV files:
  - Version 7 of package data files, with fixed LaTeX and HTML particle names.
  - Added newly-ish defined particles for two-Higgs-doublet scenario
    and additional SU(2)xU(1) groups.
  - Internal and user-irrelevant file `particle2008.csv` file removed.
- Tests:
  - Test suite extended to deal with new PDG ID related functions.
- Documentation:
  - Demo notebook slightly extended.
  - More explanations in the functions qualifying PDG IDs.
- Miscellaneous:
  - LaTeX-to-HTML particle name conversion function fixed to correctly
    deal with names containing `\prime` and/or `\tilde`.


Version 0.11.0
--------------

August 13th, 2020

- Data files:
    - Added the 2020 PDG data table .mcd file, now default.
    - Version 6 of package CSV data files:
        - Since PDG 2020 information now the default.
        - Bug fix in parity of antibaryons.
- Documentation:
    - README updated and expanded with info on custom data loading.
- Miscellaneous:
    - ZipApp fix for releasing from web interface.


Version 0.10.0
--------------

May 21th, 2020

- `Particle` class:
    - Several improvements, in particular to better deal with nuclei
        and diquarks.
    - Speed of table loading improved.
    - Particle enums extended for diquarks.
    - Make particle literals available from top-level import.
    - Print-outs made more consistent for missing and non-relevant
        particle properties.
    - New tests added, some static type checking.
- `PDGID` class:
    - PDG ID functions extended to correctly and consistently deal
        with nuclei.
    - Functions now accept any SupportsInt, including Particle objects.
- Data CSV files:
    - Version 5 of package data files:
        - Diquarks added.
        - Information in nuclei added! List and masses taken from
            package `periodictable` version 1.5.2.
        - A couple of PDG ID numbers corrected (they had evolved in
            time).
    - Converter script adapted to add to the produced data files
        particles not in the PDG data table, such as diquarks.
- Redesigned packaging system, GHA deployment.
- Miscellaneous:
    - Files `*requirements.txt` removed from package - use
        `pip install .[dev]` instead
    - Warning from `collections.abc` fixed, keeping compatibility with
        Python 2.
    - Deprecation warning in `attr.s` fixed, requirement on minimal
        version of `attr` added.
    - Version tags now follow standard `v#.#.#` format.
    - Some Python warnings fixed, warnings enabled on testing
    - Some initial work on static type hints.
    - ZipApp fixes, simplifications and size reduction; ZipApp now
        requires `python3` to be available

Version 0.9.2
-------------

February 14th, 2020

- `Particle` class:
    - Deal with particles with no mass info.
    - Make `Particle.dump_table()` work better in notebooks.

Version 0.9.1
-------------

January 14th, 2020

- `Particle` class:
    - Documentation added to various methods.
    - Minor fix to class method `from_evtgen_name(...)`.

Version 0.9.0
-------------

January 7th, 2020

- `Particle` class:
    - Robust handling of missing mass info.
- Data CSV files:
    - Version 4 of package data files, with more particles added
        (mostly badly-known particles relevant for MC).
    - Version header now also present in the `particleXXXX.csv` files.

Version 0.8.1
-------------

December 14th, 2019

- Fix of lifetimes/widths (unknown) for corner cases.
- Documentation updates.

Version 0.8.0
-------------

December 3rd, 2019

- Changes in API:
    - `GeantID` class renamed to `Geant3ID`.
- Data CSV files:
    - Version 3 (and 2) of package data files, which contain new
        entries and fixes for certain information in 2008 PDG extended
        data file.
    - File `data/pdgid_to_geantid.csv` renamed to
        `data/pdgid_to_geant3id.csv`.
    - 2016 and 2017 PDG data files `mass_width_2016.mcd` and
        `mass_width_2017.mcd` removed.
- Tests:
    - Tests for `converters` submodule added.
    - Tests for `Geant3ID` extended.
- Miscellaneous:
    - Package files formatted with `Black` package.

Version 0.7.1
-------------

November 22nd, 2019

- `Particle` class:
    - Isospin property returns a float.
    - New property `is_unflavoured_meson`.
    - More tests for P and C quantum numbers.
- `PDGID` class:
    - Non-robust P and C properties removed.
- Data CSV files:
    - Versioning introduced, see comment on first line of files.
    - File `data/pdgid_to_evtgenname.csv` extended with extra
        information.
    - More documentation.
- MC particle identification code converters:
    - Core `BiMap` class simplified.

Version 0.7.0
-------------

November 19th, 2019

- Enhancements to `Particle` class:
    - Dummy/unknown particle width and lifetime errors stored as
        `None`.
    - More particle name and `PDGID` literals for b-baryons.
    - Fix for the `D(s2)*(2573)` LaTeX name.
    - `InvalidParticle` made available at top-level import.
- Changes in API:
    - `Particle.from_dec...()` renamed to
        `Particle.from_evtgen_name(...)`.
- MC particle identification code converters:
    - Introduced directional maps `PDG2EvtGenNameMap` and
        `EvtGen2PDGNameMap` between PDG and EvtGen names.
    - Conversions master file `data/conversions.csv` added.
    - Content of converters CSV files are now ordered.
- Documentation:
    - README updated with new package functionality.
- Support for Python 3.4 removed and support for Python 3.8 added.

Version 0.6.2
-------------

September 19th, 2019

- Fix for inconsistent PDG ID and name of Upsilon\_2(1D).
- Several fixes for renames of particle names by the PDG.

Version 0.6.1
-------------

September 6th, 2019

- Enhancement to `Particle.dump_table()`.
- Added tests for Pythia and Geant identification code converters.
- Particle table CSV file updated for PDG change of 3 particle names.

Version 0.6.0
-------------

September 1st, 2019

- Introduction of classes for MC particle identification codes:
    - `PythiaID` class.
    - `GeantID` class.
- Introduction of MC particle identification code converters:
    - Generic `BiMap` bi-bidirectional map class.
    - `Pythia2PDGIDBiMap` bi-directional map between PDG and Pythia
        IDs.
    - `Geant2PDGIDBiMap` bi-directional map between PDG and Geant IDs.
    - `EvtGenName2PDGIDBiMap` bi-directional map between PDG IDs and
        EvtGen names.
- New data files:
    - File `data/pdgid_to_pythiaid.csv` for PDGID-PythiaID
        conversions.
    - File `data/pdgid_to_geantid.csv` for PDGID-GeantID conversions.
    - File `data/pdgid_to_evtgenname.csv` for PDG ID - EvtGen name
        conversions.

Version 0.5.2
-------------

August 26th, 2019

- Better handling of LaTeX to HTML conversions of particle names.
- Added the tabulate package dependency to the zipapp.

Version 0.5.1
-------------

August 21st, 2019

- Added `Particle.dump_table(...)` method.
- Added tests for default/dummy particle (PDG ID = mass = 0).
- Demo notebook updated.
- Doctests introduced in the CI.
- Dependency on package `six` removed.

Version 0.5.0
-------------

June 14th, 2019

- Added the 2019 PDG data table, now default.
    - Some poorly established particles not in the current PDG data
        files were previously erroneously made available. They have now
        been removed.

- Changes in API:
    - `Particle.table()` renamed to `Particle.all()`.

- Enhancements to `Particle` class:
    - Numerous LaTeX particle names updated.
    - Correctly deal with experimental width upper limits.
    - Better display of lifetimes and widths.
    - More tests.

- Demo notebook added, with a launcher for Binder in the README.

- Extra tests for particle searches.

Version 0.4.4
-------------

May 13th, 2019

- Setup improvements.
- zipapp CI added.
- Particle search methods made robust against exceptions.

Version 0.4.3
-------------

May 10th, 2019

- Searches given a .dec decay file particle name:
    - Speed-up of searches.
    - Corner cases dealt with.
    - Extended test suite for the `Particle.from_dec(...)` method.
- Added Particle.is\_self\_conjugate property.
- Bug fix in the PDG extended file from 2008 (in excited K, D and B
    meson names).

Version 0.4.2
-------------

April 29th, 2019

- Added re-release of the 2018 PDG data table (neutrinos added,
    formatting fixes).
- CI scripts for Azure enhanced.
- Test coverage improvements.
- Wheel now available on PyPI.

Version 0.4.1
-------------

April 2th, 2019

- Enhancements to `Particle` class:
    - Particles in .dec decay files dealt with, see
        `Particle.from_dec(...)` method.
    - Loading tables made nicer, with more documentation.
    - Particle charge is an entry of CSV files again, so that user
        particles are better dealt with.
- Bug fix for corner cases of using the package for non-valid
    particles.
- Work on documentation.
- PyPI badge created from <https://img.shields.io>.

Version 0.4.0
-------------

March 20th, 2019

- Changes in API:
    - Rename `Particle.from_search/from_search_list` to `Particle.find/findall`.
    - Rename `Particle.fullname/name` to `Particle.name/pdg_name`.
    - Rename `Particle.bar` to `Particle.is_name_barred`.
    - Rename `Particle.latex` to `Particle.latex_name`.

- Neutrinos added to the 2018 data files.

- Better print-out of particle properties.

- Better handling of particle names in HTML and LaTeX.

- Better handling of `Particle.empty()`.

- Test suite of `particle` and `pdgid` submodules improved and extended.

- Comprehensive package documentation (data files, `particle` and
    `pdgid` submodules).

- Added utility conversion function of particle names from LaTeX to
    HTML.

- Fixed LaTeX names of Delta(1232) baryons in
    `data\pdgid_to_latex.csv` file.

- Several bug fixes.

- Simpler usage of `particle.particle.convert` (non-public helper
    module).

Version 0.3.0
-------------

March 6th, 2019

- `Particle` search engine replaced with more intuitive and powerful
    version.
- Various improvements in the handling of particle names and literals.
- List of literals extended.
- More documentation in `Particle` class.
- More tests; table generation is now tested as well.
- Bug fixes in CSV data files and LaTeX naming updates.
- Added missing particles for 2018 data files.

Version 0.2.2
-------------

Feb 5th, 2019

- Bug fix in `setup.py`.
- CHANGELOG file added.

Version 0.2.1
-------------

Feb 4th, 2019

- `Particle` now has direct lifetime and ctau access.
- Better documentation.
- Several bugs fixed in `Particle` and `PDGID`.
- The minimum version of dependencies are now more accurate.

The Scikit-HEP package `hepunits` is now a strict dependency.

Version 0.2.0
-------------

Jan 29, 2019

Particle provides a pythonic interface to the Particle Data Group (PDG)
particle data tables and particle identification codes.

Version 0.1.0
-------------

Dec 19, 2018

First release, Python version of HepPID.
