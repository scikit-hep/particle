'''
This is a conversion file, used by ConvertParticleDB.ipynb.

This file requires pandas. But most users will not need this file, as it only
converts PDG files into the CSV file the other tools use.

Usage
-----

You can load a table from a classic "extended" style PDG table (only produced in 2008),
combined with a LaTeX file:


    full_table = get_from_pdg_extended('particle/data/mass_width_2008.csv',
                                       'particle/data/pdgid_to_latex.txt')

You can also read in modern file (this will produce fewer columns):

    ext_table = get_from_pdg_mcd('particle/data/mass_width_2018.mcd')

A utility is even provided to use the modern table to update the full table:

    new_table = update_from_mcd(full_table, ext_table)

You can see what particles were missing from the full table if you want:

    rem = set(ext_table.index) - set(full_table.index)
    print(ext_table.loc[rem].sort_index())

When you are done, you can save one or more of the tables:

    full_table.to_csv('particle2008.csv', float_format='%.8g')

'''

import pandas as pd

from .enums import (SpinType, Par, Charge, Inv, Status,
                    Par_mapping, Inv_mapping, Status_mapping,
                    Charge_mapping)

def get_from_latex(filename):
    """
    Produce a pandas series from a file with latex mappings in itself.
    The file format is the following: PDGID, ParticleLatexName.
    """
    latex_table = pd.read_csv(filename, index_col=0)
    return latex_table.particle

def get_from_pdg_extended(filename, latexes=None, skiprows=None):
    'Read a file, plus a list of latex files, to produce a pandas DataFrame with particle information'

    def unmap(mapping):
        return lambda x: mapping[x.strip()]

    # Convert each column from text to appropriate data type
    PDG_converters = dict(
        Charge=unmap(Charge_mapping),
        G=unmap(Par_mapping),
        P=unmap(Par_mapping),
        C=unmap(Par_mapping),
        Anti=unmap(Inv_mapping),
        Rank=lambda x: int(x.strip()) if x.strip() else 0,
        ID=lambda x: int(x.strip()) if x.strip() else -1,
        Status=unmap(Status_mapping),
        Name=lambda x: x.strip(),
        I=lambda x: x.strip(),  # noqa: E741
        J=lambda x: x.strip(),
        Quarks=lambda x: x.strip()
    )

    # Read in the table, apply the converters, add names, ignore comments
    pdg_table = pd.read_csv(filename, skiprows=skiprows, names='Mass,MassUpper,MassLower,Width,WidthUpper,WidthLower,I,G,J,P,C,Anti,'
                            'ID,Charge,Rank,Status,Name,Quarks'.split(','),
                            converters=PDG_converters
                            )

    # Read the latex
    latex_series = pd.concat([get_from_latex(latex) for latex in latexes])


    # Filtering out non-particles (quarks, negative IDs)
    # pdg_table = pdg_table[pdg_table.Charge != Par.u]
    pdg_table = pdg_table[pdg_table.ID >= 0]

    # PDG's ID should be the key to table
    pdg_table.set_index('ID', inplace=True)

    # Assign the positive values LaTeX names
    pdg_table = pdg_table.assign(Latex=latex_series)

    # Some post processing to produce inverted particles
    pdg_table_inv = pdg_table[(pdg_table.Anti == Inv.Full)
                              | ((pdg_table.Anti == Inv.Barless)
                                 # Maybe add?    & (pdg_table.Charge != Par.u)
                                 & (pdg_table.Charge != Charge.o))].copy()

    pdg_table_inv.index = -pdg_table_inv.index
    pdg_table_inv.Quarks = (pdg_table_inv.Quarks.str.swapcase()
                            .str.replace('SQRT', 'sqrt')
                            .str.replace('P', 'p').str.replace('Q', 'q')
                            .str.replace('mAYBE NON', 'Maybe non')
                            .str.replace('X', 'x').str.replace('Y', 'y'))

    full_inversion = pdg_table_inv.Anti == Inv.Full
    pdg_table_inv.Latex.where(~full_inversion,
                              pdg_table_inv.Latex.str.replace(r'^(\\mathrm{|)([\w\\]\w*)', r'\1\\bar{\2}'),
                              inplace=True)
    pdg_table_inv.Latex = pdg_table_inv.Latex.str.replace(r'+', r'%').str.replace(r'-', r'+').str.replace(r'%', r'-')

    # Make a combined table with + and - ID numbers
    full = pd.concat([pdg_table, pdg_table_inv])

    # This will override any negative values
    full.Latex.update(latex_series)

    # These items are not very important - can be reconstructed from the PDG
    del full['Charge'], full['J']

    # Nice sorting
    full['TmpVals'] = abs(full.index - .25)
    full.sort_values('TmpVals', inplace=True)
    del full['TmpVals']

    # This should be absolue value
    for name in ('MassLower', 'WidthLower'):
        full[name] = abs(full[name])

    # Return the table, making sure NaNs are just empty strings, and sort
    return full.fillna('')

def get_from_pdg_mcd(filename, skiprows=range(38)):
    '''
    Reads in a current-style PDG file (2018 tested)
    '''

    # The format here includes the space before a column
    # in the column - needed for bug in file alignment 2018
    #
    # Also, we can't use * as a comment char, since it is valid
    # in the particle names, as well!

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
        skiprows=skiprows, header=None, names=(
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

    # This should be in MeV, not GeV, and absolue value
    for name in ('Mass', 'MassUpper', 'MassLower', 'Width', 'WidthUpper', 'WidthLower'):
        ds[name] = abs(ds[name]*1000)


    return ds

def update_from_mcd(full_table, update_table):
    'Update existing particles only'

    full_table = full_table.copy()
    full_table.update(update_table)
    update_table_neg = update_table.copy()
    update_table_neg.index = -update_table_neg.index
    full_table.update(update_table_neg)

    return full_table
