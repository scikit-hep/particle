# This is a conversion file

# This file requires pandas. But most users will not need this file, as it only
# converts into the CSV file the other tools use.

import pandas as pd

from .enums import (SpinType, Par, Charge, Inv, Status,
                    Par_mapping, Inv_mapping, Status_mapping)

def get_from_latex(filename):
    """
    Produce a pandas series from a file with latex mappings in itself.
    The file format is the following: PDGID ParticleLatexName AntiparticleLatexName.
    """
    latex_table = pd.read_csv(filename, index_col=0)
    series_real = latex_table.particle
    series_anti = latex_table.antiparticle
    series_anti.index = -series_anti.index
    return pd.concat([series_real, series_anti])

def get_from_pdg_extended(filename, latexes=None):
    'Read a file, plus a list of latex files, to produce a pandas DataFrame with particle information'

    def unmap(mapping):
        return lambda x: mapping[x.strip()]

    # Convert each column from text to appropriate data type
    PDG_converters = dict(
        Charge=unmap(Par_mapping),
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
    pdg_table = pd.read_csv(filename, comment='*', names='Mass,MassUpper,MassLower,Width,WidthUpper,WidthLower,I,G,J,P,C,Anti,'
                            'ID,Charge,Rank,Status,Name,Quarks'.split(','),
                            converters=PDG_converters
                            )

    # Filtering out non-particles (quarks, negative IDs)
    pdg_table = pdg_table[pdg_table.Charge != Par.u]
    pdg_table = pdg_table[pdg_table.ID >= 0]
    
    # PDG's ID should be the key to table
    pdg_table.set_index('ID', inplace=True)
    
    # Note that 313 should have (892) in the name.
    if 313 in pdg_table.index and  '(892)' not in pdg_table.loc[313, 'Name']:
        pdg_table.loc[313, 'Name'] += '(892)'

    # Some post processing to produce inverted particles
    pdg_table_inv = pdg_table[(pdg_table.Anti == Inv.Full)
                              | ((pdg_table.Anti == Inv.Barless)
                                 # Maybe add?    & (pdg_table.Charge != Par.u)
                                 & (pdg_table.Charge != Par.o))].copy()
    pdg_table_inv.index = -pdg_table_inv.index
    pdg_table_inv.Quarks = (pdg_table_inv.Quarks.str.swapcase()
                            .str.replace('SQRT', 'sqrt')
                            .str.replace('P', 'p').str.replace('Q', 'q')
                            .str.replace('mAYBE NON', 'Maybe non')
                            .str.replace('X', 'x').str.replace('Y', 'y'))
    
    # Make a combined table with + and - ID numbers
    full = pd.concat([pdg_table, pdg_table_inv])

    # Add the latex
    if latexes is None:
        latexes = (open_text(data, 'pdgID_to_latex.txt'),)

    latex_series = pd.concat([get_from_latex(latex) for latex in latexes])
    full = full.assign(Latex=latex_series)

    # These items are not very important - can be reconstructed from the PDG
    del full['Charge'], full['J']
    
    # This should be in GeV, not MeV
    for name in ('Mass', 'MassUpper', 'MassLower', 'Width', 'WidthUpper', 'WidthLower'):
        full[name] /= 1000

    # Nice sorting
    full['TmpVals'] = abs(full.index - .25)
    full.sort_values('TmpVals', inplace=True)
    del full['TmpVals']
    
    # Return the table, making sure NaNs are just empty strings, and sort
    return full.fillna('')

def get_from_pdg_mcd(filename):
    '''
    Reads in a current-style PDG file (2018 tested)
    '''
    nar = pd.read_fwf(filename, comment='*', colspecs=(
        (0,8),
        (8,16),
        (16,24),
        (24,32),
        (33,51),
        (52,60),
        (61,69),
        (70,88),
        (89,97),
        (98,106),
        (107,128),
        ),
        skiprows=None, header=None, names=(
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
        
    return ds

def update_from_mcd(full_table, update_table):
    'Update existing particles only'

    full_table = full_table.copy()
    full_table.update(update_table)
    update_table_neg = update_table.copy()
    update_table_neg.index = -update_table_neg.index
    full_table.update(update_table_neg)
    
    return full_table