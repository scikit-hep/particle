Particle Data folder contents
-----------------------------

You can ``import particle.data``, then use ``particle.data.open_text(particle.data, 'particle2018.csv')``
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


``mass_width_2018.mcd``
=======================

The current style PDG data file, with much less information, but with more particles and more up to date.
A few older years are included, too.


``pdgid_to_latex.csv``
======================

A list of PDG IDs and LaTeX names. The negative values are normally generated based on the ``Inv`` rule,
but if you have a special case, you can set a negative value as well and it will override.


``particle2018.csv``
====================

The combined data file, in a format that is easy for the ``Particle`` class to read and easy for physicists to extend or edit.
If you'd like to append to this file, write a similar file with the same header, then use

.. code-block:: python

    Particle.read_table()
    Particle.read_table('...', append=True)

to read in the original table and then the new file you've written.

This file was created from ``pdgid_to_latex.csv``, ``mass_width_2008.fwf``, ``mass_width_2008_ext.fwf``
and ``mass_width_2018.mcd``.
The 2008 version of the file was created with only the first two.
