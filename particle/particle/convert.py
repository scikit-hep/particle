# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

'''
This is a conversion file, not part of the public API.

The default CSV files can be updated directly using the command:

    >>> python -m particle.particle.convert regenerate 2018

A custom fwf file and LaTeX file can be converted into the CSV format using:

    >>> python -m particle.particle.convert extended file.fwf latex.csv output.csv

This file requires pandas. But most users will not need this file, as it only
converts PDG data files into the CSV file(s) the public API tools use. The tests
load some of these functions to verify the CSV files are in sync with the sources.

Internal usage
--------------

You can load a table from a classic "extended style" PDG table (only produced in 2008),
combined with one or more LaTeX files describing the pair (PDG ID, LaTeX name):

    >>> full_table = get_from_pdg_extended('particle/data/mass_width_2008.fwf',
    ...                                    ['particle/data/pdgid_to_latex.csv'])

You can also read in a modern "standard" file (this will produce fewer columns):

    >>> ext_table = get_from_pdg_mcd('particle/data/mass_width_2018.mcd')

A utility is even provided to use the modern table to update the full table:

    >>> new_table = update_from_mcd(full_table, ext_table)

You can see what particles were missing from the full table if you want:

    >>> rem = set(ext_table.index) - set(full_table.index)
    >>> print(ext_table.loc[rem].sort_index())

When you are done, you can save one or more of the tables:

    >>> full_table.to_csv('particle2008.csv', float_format='%.8g')

'''

import os
FILE_DIR = os.path.dirname(os.path.realpath(__file__))

import pandas as pd
import six

from .enums import (SpinType, Parity, Charge, Inv, Status,
                    Parity_mapping, Inv_mapping, Status_mapping,
                    Charge_mapping)

from .. import data


def get_from_latex(filename):
    """
    Produce a pandas series from a file with LaTeX mappings in itself.
    The CVS file format is the following: PDGID, ParticleLatexName.
    """
    latex_table = pd.read_csv(filename, index_col=0)
    return latex_table.particle


def filter_file(fileobject):
    """
    Open a file if not already a file-like object, and strip lines that start with *.
    Returns a new file-like object (StringIO instance).
    """

    if not hasattr(fileobject, 'read'):
        fileobject = open(fileobject)

    stream = six.StringIO()
    for line in fileobject:
        # We need to strip the unicode byte ordering if present before checking for *
        if not line.lstrip('\ufeff').lstrip().startswith('*'):
            stream.write(line)
    stream.seek(0)
    return stream


def get_from_pdg_extended(filename, latexes=None):
    """
    Read an "extended style" PDG data file (only produced in 2008), plus a list of LaTeX files,
    to produce a pandas DataFrame with particle information.

    Parameters
    ----------
    filename: string
        Input file name
    latexes: list
        A list of names of LaTeX files describing the pair (PDG ID, LaTeX name) in CSV format

    Example
    -------
    >>> full_table = get_from_pdg_extended('particle/data/mass_width_2008.fwf',
    ...                                    ['particle/data/pdgid_to_latex.csv'])
    """
    'Read a file, plus a list of LaTeX files, to produce a pandas DataFrame with particle information'

    def unmap(mapping):
        return lambda x: mapping[x.strip()]

    # Convert each column from text to appropriate data type
    PDG_converters = dict(
        Charge=unmap(Charge_mapping),
        G=unmap(Parity_mapping),
        P=unmap(Parity_mapping),
        C=unmap(Parity_mapping),
        Anti=unmap(Inv_mapping),
        Rank=lambda x: int(x.strip()) if x.strip() else 0,
        ID=lambda x: int(x.strip()) if x.strip() else -1,
        Status=unmap(Status_mapping),
        Name=lambda x: x.strip(),
        I=lambda x: x.strip(),  # noqa: E741
        J=lambda x: x.strip(),
        Quarks=lambda x: x.strip()
    )

    filename = filter_file(filename)

    # Read in the table, apply the converters, add names, ignore comments
    pdg_table = pd.read_csv(filename, names='Mass,MassUpper,MassLower,Width,WidthUpper,WidthLower,I,G,J,P,C,Anti,'
                            'ID,Charge,Rank,Status,Name,Quarks'.split(','),
                            converters=PDG_converters
                            )

    # Read the LaTeX
    latex_series = pd.concat([get_from_latex(latex) for latex in latexes])


    # Filtering out non-particles (quarks, negative IDs)
    # pdg_table = pdg_table[pdg_table.Charge != Charge.u]
    pdg_table = pdg_table[pdg_table.ID >= 0]

    # PDG's ID should be the key to table
    pdg_table.set_index('ID', inplace=True)

    # Assign the positive values LaTeX names
    pdg_table = pdg_table.assign(Latex=latex_series)

    # Some post processing to produce inverted particles
    pdg_table_inv = pdg_table[(pdg_table.Anti == Inv.Barred)
                              | ((pdg_table.Anti == Inv.ChargeInv)
                                 # Maybe add?    & (pdg_table.Charge != Charge.u)
                                 & (pdg_table.Charge != Charge.o))].copy()

    pdg_table_inv.index = -pdg_table_inv.index
    pdg_table_inv.Charge = -pdg_table_inv.Charge
    pdg_table_inv.Quarks = (pdg_table_inv.Quarks.str.swapcase()
                            .str.replace('SQRT', 'sqrt')
                            .str.replace('P', 'p').str.replace('Q', 'q')
                            .str.replace('mAYBE NON', 'Maybe non')
                            .str.replace('X', 'x').str.replace('Y', 'y'))

    full_inversion = pdg_table_inv.Anti == Inv.Barred
    pdg_table_inv.Latex.where(~full_inversion,
                              pdg_table_inv.Latex.str.replace(r'^(\\mathrm{|)([a-zA-Z\\][a-zA-Z]*)', r'\1\\bar{\2}'),
                              inplace=True)
    pdg_table_inv.Latex = pdg_table_inv.Latex.str.replace(r'+', r'%').str.replace(r'-', r'+').str.replace(r'%', r'-')

    # Make a combined table with + and - ID numbers
    full = pd.concat([pdg_table, pdg_table_inv])

    # This will override any negative values
    full.Latex.update(latex_series)

    # These items are not very important - can be reconstructed from the PDG ID
    # TODO: maybe first check the consistency between what is read in and what the PDG ID provides (being maniac)?
    del full['J']

    # Nice sorting
    sort_particles(full)

    # This should be absolue value
    for name in ('MassLower', 'WidthLower'):
        full[name] = abs(full[name])

    # Return the table, making sure NaNs are just empty strings, and sort
    return full.fillna('')


def sort_particles(table):
    "Sort a particle list table nicely"
    table['TmpVals'] = abs(table.index - .25)
    table.sort_values('TmpVals', inplace=True)
    del table['TmpVals']


def get_from_pdg_mcd(filename):
    '''
    Reads in a current-style PDG .mcd file (mass_width_2018.mcd file tested).

    Example
    -------
    >>> mcd_table = get_from_pdg_mcd('particle/data/mass_width_2018.mcd')
    '''

    # The format here includes the space before a column
    # in the column - needed for bug in file alignment 2018
    #
    # Also, we can't use * as a comment char, since it is valid
    # in the particle names, as well!

    filename = filter_file(filename)

    nar = pd.read_fwf(filename, colspecs=(
        (0,8),
        (8,16),
        (16,24),
        (24,32),
        (32,51),
        (51,60),
        (60,69),
        (69,88),
        (88,97),
        (97,106),
        (106,128),
        ),
        header=None, names=(
        'ID1', 'ID2', 'ID3', 'ID4',
            'Mass', 'MassUpper', 'MassLower',
            'Width', 'WidthUpper', 'WidthLower',
            'NameCharge'))

    ds = []
    for i in range(4):
        name = 'ID{0}'.format(i+1)
        d = nar[~pd.isna(nar[name])].copy()
        d['ID'] = d[name].astype(int)
        nc = d.NameCharge.str.split(expand=True)
        d['Name'] = nc[0]
        abcd = nc[1].str.split(',', 4, expand=True)
        d['charge'] = abcd[i]
        d.set_index('ID', inplace=True)
        ds.append(d)

    ds = pd.concat(ds)
    del ds['NameCharge'], ds['ID1'], ds['ID2'], ds['ID3'], ds['ID4']
    ds.sort_index(inplace=True)

    # This should be in MeV, not GeV, and absolute value
    for name in ('Mass', 'MassUpper', 'MassLower', 'Width', 'WidthUpper', 'WidthLower'):
        ds[name] = abs(ds[name]*1000)


    return ds


def update_from_mcd(full_table, update_table):
    """
    Update the full table (aka the PDG extended-style table) with the up-to-date information
    from the PDG .mcd file for all existing particles in the latter.

    Example
    -------
    >>> new_table = update_from_mcd('mass_width_2008.fwf', 'mass_width_2018.mcd')
    """

    full_table = full_table.copy()
    full_table.update(update_table)
    update_table_neg = update_table.copy()
    update_table_neg.index = -update_table_neg.index
    full_table.update(update_table_neg)

    return full_table


def produce_files(particle2008, particle2018, year):
    'This produces listed output files from all input files.'


    full_table = get_from_pdg_extended(data.open_text(data, 'mass_width_2008.fwf'),
                                       [data.open_text(data, 'pdgid_to_latex.csv')])

    # Entries to remove, see comments in file mass_width_2008_ext.fwf:
    # 30221 - the f(0)(1370) since it was renumbered
    # 100223 - the omega(1420) since it was renumbered
    # 5132 and 5232 - the Xi_b baryons got their IDs swapped at some stage
    full_table.drop([30221, 100223, 5132, 5232], axis=0, inplace=True)

    full_table.to_csv(particle2008, float_format='%.12g')

    addons = get_from_pdg_extended(data.open_text(data, 'mass_width_2008_ext.fwf'),
                                   [data.open_text(data, 'pdgid_to_latex.csv')])

    full_table = pd.concat([full_table, addons])

    # Allow replacement of particles by the ext file
    full_table = full_table[~full_table.index.duplicated(keep='last')]

    sort_particles(full_table)

    ext_table = get_from_pdg_mcd(data.open_text(data, 'mass_width_'+year+'.mcd'))
    new_table = update_from_mcd(full_table, ext_table)

    new_table.to_csv(particle2018, float_format='%.12g')


def main(year):
    'Regenerate output files - run directly inside the package'
    master_dir = os.path.dirname(FILE_DIR)
    data_dir = os.path.join(master_dir, 'data')
    particle2008 = os.path.join(data_dir, 'particle2008.csv')
    particlenew = os.path.join(data_dir, 'particle'+year+'.csv')

    produce_files(particle2008, particlenew, year)


def convert(fwf, latex, output):
    table = get_from_pdg_extended(fwf,
                                  [data.open_text(data, 'pdgid_to_latex.csv'),
                                   latex])

    table.to_csv(output, float_format='%.12g')


def run_regen(args):
    main(args.year)


def run_convert(args):
    convert(args.fwf, args.latex, args.output)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help='Options (pick one)')
    subparsers.required = True
    subparsers.dest = 'command'

    parser_regen = subparsers.add_parser('regenerate', help='Regenerate the built in files from the built in names')
    parser_regen.add_argument('year', help='Year of file to read in/produce (2008 is always read/produced)')
    parser_regen.set_defaults(func=run_regen)

    parser_convert = subparsers.add_parser('extended', help='Make a new file from extended inputs')
    parser_convert.add_argument('fwf', type=FileType('r'),  help='Fixed width format extended file')
    parser_convert.add_argument('latex', type=FileType('r'), help='Latex file with names')
    parser_convert.add_argument('output', type=FileType('w'), help='Output file name')
    parser_convert.set_defaults(func=run_convert)

    args = parser.parse_args()
    args.func(args)
