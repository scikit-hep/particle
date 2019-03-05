import pytest
import sys

# Requires pandas
pd = pytest.importorskip('pandas')

from particle import data
from particle.particle.convert import produce_files

def test_generate(tmp_path):
    'This verifies that the input and output files match.'

    particle2008 = tmp_path / 'particle2008.csv'
    particle2018 = tmp_path / 'particle2018.csv'

    produce_files(particle2008, particle2018)

    particle2008_data = data.open_text(data, 'particle2008.csv')
    with particle2008.open() as src, particle2008_data as res:
        assert src.read() == res.read()

    particle2018_data = data.open_text(data, 'particle2018.csv')
    with particle2018.open() as src, particle2018_data as res:
        assert src.read() == res.read()
