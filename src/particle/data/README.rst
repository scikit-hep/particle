Particle Data folder contents
-----------------------------

You can ``import particle.data``, then use ``particle.data.basepath / "particle2022.csv"``
to access data reliably regardless of how you have installed or are running the package (even from a zip file!).


``mass_width_2008.fwf``
=======================

The extended PDG data file, produced once, in 2008. This is the basis for the particle information.
This file originally had a CSV extension, but it not a comma separated value file, but rather a fixed
width format.


``mass_width_2008_ext.fwf``
===========================

An extension file for the extended PDG data file, prepared by this package's maintainers.
It contains entries necessary to provide extended information for the particles in the standard .mcd file.


``mass_width_2022.mcd``
=======================

The latest version of the PDG particle data file, downloaded from the PDG website
(renamed from .txt to the .mcd extension as in previous years),
with much less information, but with more particles and more up to date.
A few older years are included, too.


``particle2022.csv``
====================

The combined data file, in a format that is easy for the ``Particle`` class to read and easy for physicists to extend or edit.
If you'd like to append to this file, write a similar file with the same header, then use

.. code-block:: python

    Particle.read_table()
    Particle.read_table('...', append=True)

to read in the original table and then the new file you've written.

This file was created from ``pdgid_to_latexname.csv``, ``mass_width_2008.fwf``,
``mass_width_2008_ext.fwf`` and ``mass_width_2022.mcd``.
The 2008 version of the file was created with only the first two.


``conversions.csv``
===================

Master conversions file containing all matching MC IDs and names.
This is the file internally used to produce all other ``x_to_y.csv`` files.
Updates to converters data should be made to this file and subsequently
propagated to the ``x_to_y.csv`` files.

This file and all ``x_to_y.csv`` files are versioned, see the first-line comments.


``pdgid_to_latexname.csv``
==========================

A list of matching particle PDG identification codes and LaTeX names.
The negative values are normally generated based on the ``Inv`` rule,
but if you have a special case, you can set a negative value as well and it will override.


``pdgid_to_pythiaid.csv``
=========================

A list of matching particle PDG and Pythia identification codes.
Note that this file contains entries for particles not in the PDG data file,
for completeness (e.g., non-yet-observed baryons, leptoquarks).


``pdgid_to_geant3id.csv``
=========================

A list of matching particle PDG and Geant3 identification codes;
Geant4 follows the PDG rules, hence uses the standard PDG IDs.
Note that this file contains entries for particles not in the PDG data file,
for completeness (e.g., non-yet-observed baryons, leptoquarks).


``pdgid_to_evtgenname.csv``
===========================

A list of matching particle PDG IDs and particle names used by EvtGen.
