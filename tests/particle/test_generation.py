
import pytest
import sys

# Requires Python 3 and pandas
pd = pytest.importorskip('pandas')

from particle import data
from particle.particle.convert import (get_from_pdg_extended,
                                       get_from_pdg_mcd,
                                       update_from_mcd)

def test_generate(tmp_path):
    'This verifies that the input and output files match.'


    full_table = get_from_pdg_extended(data.open_text(data, 'mass_width_2008.fwf'),
                                   [data.open_text(data, 'pdgid_to_latex.csv')],
                                   skiprows=list(range(100)) + list(range(495,499)))


    particle2008 = tmp_path / 'particle2008.csv'
    full_table.to_csv(particle2008, float_format='%.12g')

    ext_table = get_from_pdg_mcd(data.open_text(data, 'mass_width_2018.mcd'))
    new_table = update_from_mcd(full_table, ext_table)

    particle2018 = tmp_path / 'particle2018.csv'
    new_table.to_csv(particle2018, float_format='%.12g')

    particle2008_data = data.open_text(data, 'particle2008.csv')
    with particle2008.open() as src, particle2008_data as res:
        assert src.read() == res.read()

    particle2018_data = data.open_text(data, 'particle2018.csv')
    with particle2018.open() as src, particle2018_data as res:
        assert src.read() == res.read()


