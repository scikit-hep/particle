Particle Data folder
--------------------

You can `import particle.data`, then use `particle.data.open_text(particle.data, 'particle2018.csv')`
to access data reliably regardless of how you have installed or are running Particle (even from a zip file!).


`mass_width_2008.fwf`
=====================

The extended PDG datafile, produced once, in 2008. This is the basis for the Particle information.
This file originally had a csv extension, but it not a comma seperated value file, but rather a fixed
width format.


`mass_width_2018.mcd`
=====================

The current style PDG data file, with much less information, but with more particles and more up to date.
A few older years are included, too.


`pdgid_to_latex.csv`
====================

A list of PDGIDs and latex names. The negative values are normally generated based on the `Inv` rule, but if you have
a special case, you can set a negitive value as well and it will override.



`particle2018.csv`
==================

The combined datafile, in a format that is easy for Paricle to read and easy for physists to extend or edit.
If you'd like to append to this file, write a similar file with the same header, then use

    Paricle.read_table()
    Particle.read_table('...', append=True)

to read in the original table and then the new file you've written.

This file was created from `pdgid_to_latex.csv`, `mass_width_2008.fwf`, and `mass_width_2018.mcd`. The 2008 version
of the file was created with only the first two.
