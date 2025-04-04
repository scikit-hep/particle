# Copyright (c) 2018-2025, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

"""
This is a conversion file, not part of the public API.

The default CSV files can be updated directly using the command:

    >>> python -m particle.particle.convert regenerate 2024 <version_number>    # doctest: +SKIP

A custom fwf file and LaTeX file can be converted into the CSV format using:

    >>> python -m particle.particle.convert extended output.csv file.fwf <version_number> latex.csv    # doctest: +SKIP

The command is typically

    >>> python -m particle.particle.convert extended output.csv src/particle/data/mass_width_2008.fwf <version_number>    # doctest: +SKIP

This file requires pandas. But most users will not need this file, as it only
converts PDG data files into the CSV file(s) the public API tools use. The tests
load some of these functions to verify the CSV files are in sync with the sources.

Internal usage
--------------

You can load a table from a classic "extended style" PDG table (only produced in 2008),
combined with one or more LaTeX files describing the pair (PDG ID, LaTeX name):

    >>> full_table = get_from_pdg_extended('particle/data/mass_width_2008.fwf',
    ...                                    ['particle/data/pdgid_to_latexname.csv'])

You can also read in a modern "standard" file (this will produce fewer columns):

    >>> ext_table = get_from_pdg_mcd('particle/data/mass_width_2024.mcd')

A utility is even provided to use the modern table to update the full table:

    >>> new_table = update_from_mcd(full_table, ext_table)

You can see what particles were missing from the full table if you want:

    >>> rem = set(ext_table.index) - set(full_table.index)
    >>> print(ext_table.loc[rem].sort_index())    # doctest: +SKIP

When you are done, you can save one or more of the tables:

    >>> full_table.to_csv('particle2008.csv', float_format='%.8g')

"""

from __future__ import annotations

import os
import warnings
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Any, Callable, Iterable, TextIO, TypeVar

import numpy as np
import pandas as pd

from .. import data
from .._compat.typing import Traversable
from ..pdgid import PDGID, is_baryon
from ..typing import StringOrIO
from .enums import (
    Charge,
    Charge_mapping,
    Inv,
    Inv_mapping,
    Parity,
    Parity_mapping,
    Status_mapping,
)

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

__all__ = (
    "convert",
    "get_from_latex",
    "get_from_pdg_extended",
    "get_from_pdg_mcd",
    "update_from_mcd",
)


def __dir__() -> tuple[str, ...]:
    return __all__


def get_from_latex(filename: StringOrIO) -> pd.Series:
    """
    Produce a pandas series from a file with LaTeX mappings in itself.
    The CVS file format is the following: PDGID, ParticleLatexName.
    """
    latex_table = pd.read_csv(filename, index_col=0, comment="#")
    return latex_table.LATEXNAME


def filter_file(fileobject: StringOrIO) -> TextIO:
    """
    Open a file if not already a file-like object, and strip lines that start with *.
    Returns a new file-like object (StringIO instance).
    """

    if not hasattr(fileobject, "read"):
        assert isinstance(fileobject, str)
        with open(fileobject, encoding="utf-8") as f:
            return filter_file(f)

    assert not isinstance(fileobject, (str, Traversable))

    stream = StringIO()
    for line in fileobject:
        # We need to strip the unicode byte ordering if present before checking for *
        if not line.lstrip("\ufeff").lstrip().startswith("*"):
            stream.write(line)
    stream.seek(0)

    return stream


T = TypeVar("T")


def get_from_pdg_extended(
    filename: StringOrIO, latexes: Iterable[StringOrIO] = ()
) -> pd.DataFrame:
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
    ...                                    ['particle/data/pdgid_to_latexname.csv'])
    """

    # Read a file, plus a list of LaTeX files, to produce a pandas DataFrame with particle information
    def unmap(mapping: dict[str, T]) -> Callable[[str], T]:
        return lambda x: mapping[x.strip()]

    # Convert each column from text to appropriate data type
    PDG_converters = {
        "Charge": unmap(Charge_mapping),
        "G": unmap(Parity_mapping),
        "P": unmap(Parity_mapping),
        "C": unmap(Parity_mapping),
        "Anti": unmap(Inv_mapping),
        "Rank": lambda x: int(x.strip()) if x.strip() else 0,
        "ID": lambda x: int(x.strip()) if x.strip() else -1,
        "Status": unmap(Status_mapping),
        "Name": lambda x: x.strip(),
        "I": lambda x: x.strip(),
        "J": lambda x: x.strip(),
        "Quarks": lambda x: x.strip(),
    }

    with filter_file(filename) as file_object:
        # Read in the table, apply the converters, add names, ignore comments
        pdg_table = pd.read_csv(
            file_object,
            names=[
                "Mass",
                "MassUpper",
                "MassLower",
                "Width",
                "WidthUpper",
                "WidthLower",
                "I",
                "G",
                "J",
                "P",
                "C",
                "Anti",
                "ID",
                "Charge",
                "Rank",
                "Status",
                "Name",
                "Quarks",
            ],
            converters=PDG_converters,
            comment="#",
        )

    # Read the LaTeX
    latex_series = pd.concat([get_from_latex(latex) for latex in latexes])

    # Filtering out non-particles (quarks, negative IDs)
    # pdg_table = pdg_table[pdg_table.Charge != Charge.u]
    pdg_table = pdg_table[pdg_table.ID >= 0]

    # PDG's ID should be the key to table
    pdg_table.set_index("ID", inplace=True)

    # Assign the positive values LaTeX names
    pdg_table = pdg_table.assign(Latex=latex_series)

    # Some post processing to produce inverted particles
    pdg_table_inv = pdg_table[
        (pdg_table.Anti == Inv.Barred)
        | (
            (pdg_table.Anti == Inv.ChargeInv)
            # Maybe add?    & (pdg_table.Charge != Charge.u)
            & (pdg_table.Charge != Charge.o)
        )
    ].copy()

    pdg_table_inv.index = -pdg_table_inv.index
    pdg_table_inv.Charge = -pdg_table_inv.Charge
    pdg_table_inv.Quarks = (
        pdg_table_inv.Quarks.str.swapcase()
        .str.replace("SQRT", "sqrt")
        .str.replace("P", "p")
        .str.replace("Q", "q")
        .str.replace("mAYBE NON", "Maybe non")
        .str.replace("X", "x")
        .str.replace("Y", "y")
    )

    # Parity flips for baryons
    def is_baryon_with_defined_parity(i: PDGID, p: Parity) -> bool:
        return is_baryon(i) and p != Parity.u

    pdg_table_inv["P"] = np.where(
        pdg_table_inv.reset_index().apply(
            lambda x: is_baryon_with_defined_parity(x["ID"], x["P"]), axis=1
        ),
        -pdg_table_inv["P"],
        pdg_table_inv["P"],
    )

    full_inversion = pdg_table_inv.Anti == Inv.Barred
    pdg_table_inv.Latex.where(
        ~full_inversion,
        pdg_table_inv.Latex.str.replace(
            r"^(\\mathrm{|)([a-zA-Z\\][a-zA-Z]*)", r"\1\\overline{\2}", regex=True
        ),
        inplace=True,
    )
    pdg_table_inv.Latex = (
        pdg_table_inv.Latex.str.replace(r"+", r"%", regex=False)
        .str.replace(r"-", r"+", regex=False)
        .str.replace(r"%", r"-", regex=False)
    )

    # Make a combined table with + and - ID numbers
    full = pd.concat([pdg_table, pdg_table_inv])

    # This will override any negative values
    full.Latex.update(latex_series)

    # These items are not very important - can be reconstructed from the PDG ID
    # TODO: maybe first check the consistency between what is read in and what the PDG ID provides (being maniac)?
    del full["J"]

    # Nice sorting
    sort_particles(full)

    # All the 'MassLower' and 'WidthLower' values should be absolute values
    # except for the special cases when they are equal to -1,
    # which flag experimental upper limits or badly known particles
    full.loc[full["MassLower"] != -1, "MassLower"] = abs(full["MassLower"])
    full.loc[full["WidthLower"] != -1, "WidthLower"] = abs(full["WidthLower"])

    # Return the table, making sure NaNs are just empty strings, and sort
    return full.fillna("")


def sort_particles(table: pd.DataFrame) -> None:
    "Sort a particle list table nicely"
    table["TmpVals"] = abs(table.index - 0.25)
    table.sort_values("TmpVals", inplace=True)
    del table["TmpVals"]


def get_from_pdg_mcd(filename: StringOrIO) -> pd.DataFrame:
    """
    Reads in a current-style PDG .mcd file (mass_width_2024.mcd file tested).

    Example
    -------
    >>> mcd_table = get_from_pdg_mcd('particle/data/mass_width_2024.mcd')
    """

    # The format here includes the space before a column
    # in the column - needed for bug in file alignment 2018
    #
    # Also, we can't use * as a comment char, since it is valid
    # in the particle names, as well!

    with filter_file(filename) as file_object:
        nar = pd.read_fwf(
            file_object,
            colspecs=(
                (0, 8),
                (8, 16),
                (16, 24),
                (24, 32),
                (32, 51),
                (51, 60),
                (60, 69),
                (69, 88),
                (88, 97),
                (97, 106),
                (106, 128),
            ),
            header=None,
            names=(
                "ID1",
                "ID2",
                "ID3",
                "ID4",
                "Mass",
                "MassUpper",
                "MassLower",
                "Width",
                "WidthUpper",
                "WidthLower",
                "NameCharge",
            ),
        )

        # Check for duplicates!
        duplicated_ids = (
            nar.duplicated(subset=["ID1"], keep=False) & nar["ID1"].notna()
            | nar.duplicated(subset=["ID2"], keep=False) & nar["ID2"].notna()
            | nar.duplicated(subset=["ID3"], keep=False) & nar["ID3"].notna()
            | nar.duplicated(subset=["ID4"], keep=False) & nar["ID4"].notna()
        )
        if nar[duplicated_ids].shape[0] > 0:
            print("DUPLICATES:\n", nar[duplicated_ids])
        assert nar[duplicated_ids].shape[0] == 0, (
            f"Duplicate entries found in {filename} !"
        )

    ds_list = []
    for i in range(4):
        name = f"ID{i + 1}"
        d = nar[~pd.isna(nar[name])].copy()
        d["ID"] = d[name].astype(int)
        nc = d.NameCharge.str.split(expand=True)
        d["Name"] = nc[0]
        abcd = nc[1].str.split(pat=",", n=4, expand=True)
        d["charge"] = abcd[i]
        d.set_index("ID", inplace=True)
        ds_list.append(d)

    ds = pd.concat(ds_list)
    del ds["NameCharge"], ds["ID1"], ds["ID2"], ds["ID3"], ds["ID4"]
    ds.sort_index(inplace=True)

    # This should be in MeV, not GeV, and absolute value
    for name in ("Mass", "MassUpper", "MassLower", "Width", "WidthUpper", "WidthLower"):
        ds[name] = abs(ds[name] * 1000)

    return ds


def update_from_mcd(
    full_table: pd.DataFrame, update_table: pd.DataFrame
) -> pd.DataFrame:
    """
    Update the full table (aka the PDG extended-style table) with the
    up-to-date information from the PDG .mcd file.

    Example
    -------
    >>> new_table = update_from_mcd('mass_width_2008.fwf', 'mass_width_2024.mcd')    # doctest: +SKIP
    """

    full_table = full_table.copy()
    full_table.update(update_table)
    update_table_neg = update_table.copy()
    update_table_neg.index = -update_table_neg.index
    full_table.update(update_table_neg)

    return full_table


def produce_files(
    particle2008: str | Path,  # noqa: ARG001
    particle2024: str | Path,
    version: str,
    year: str,
) -> None:
    "This produces listed output files from all input files."

    with data.basepath.joinpath("mass_width_2008.fwf").open() as fwf_f:  # noqa: SIM117
        with data.basepath.joinpath("pdgid_to_latexname.csv").open() as csv_f:
            full_table = get_from_pdg_extended(fwf_f, [csv_f])

    # Entries to remove, see comments in file mass_width_2008_ext.fwf:
    # 30221 - the f(0)(1370) since it was renumbered
    # 5132 and 5232 - the Xi_b baryons got their IDs swapped at some stage
    full_table.drop([30221, 5132, 5232], axis=0, inplace=True)

    # No longer write out the particle2008.csv file, which nobody should use
    # with open(particle2008, "w", newline="\n", encoding="utf-8") as f:
    # f.write(version_header(particle2008, version))
    # full_table.to_csv(f, float_format="%.12g")

    with data.basepath.joinpath("mass_width_" + year + ".mcd").open() as mcd_f:
        ext_table = get_from_pdg_mcd(mcd_f)

    with data.basepath.joinpath(
        "mass_width_2008_ext.fwf"
    ).open() as fwf_f, data.basepath.joinpath("pdgid_to_latexname.csv").open() as csv_f:
        addons = get_from_pdg_extended(fwf_f, [csv_f])

    # Only keep rows present in the .mcd file specified by year
    full_table = full_table[
        full_table.index.isin(ext_table.index) | full_table.index.isin(-ext_table.index)
    ]

    # Check it there are rows only present in the .mcd file specified by year,
    # in which case we need to update our curated files!
    ext_table_excl = pd.DataFrame(
        ext_table[
            ~(
                ext_table.index.isin(full_table.index)
                | ext_table.index.isin(addons.index)
            )
        ],
        columns=full_table.columns,
    )
    if len(ext_table_excl) > 0:
        mcd_year = "mass_width_" + year + ".mcd"
        warnings.warn(
            f"""{mcd_year!r} contains the following {len(ext_table_excl)} new entries:"
    {ext_table_excl.index.to_list()}
    Curation needs an update!""",
            stacklevel=1,
        )

    full_table = pd.concat([full_table, addons])

    # Allow replacement of particles by the ext file
    full_table = full_table[~full_table.index.duplicated(keep="last")]

    sort_particles(full_table)

    new_table = update_from_mcd(full_table, ext_table)

    with open(particle2024, "w", newline="\n", encoding="utf-8") as f:
        f.write(version_header(str(particle2024), version))
        new_table.to_csv(f, float_format="%.12g")


def version_header(filename: str, version_number: str) -> str:
    filename = os.path.basename(filename)
    version = version_number  # version of CSV files
    today_date = date.isoformat(date.today())
    return f"# (c) Scikit-HEP project - Particle package data file - {filename} - version {version} - {today_date}\n"


def main(version: str, year: str) -> None:
    "Regenerate output files - run directly inside the package"
    main_dir = os.path.dirname(FILE_DIR)
    data_dir = os.path.join(main_dir, "data")
    particle2008 = os.path.join(data_dir, "particle2008.csv")
    particlenew = os.path.join(data_dir, "particle" + year + ".csv")

    produce_files(particle2008, particlenew, version, year)


def convert(version: str, output: str, fwf: str, latex: str | None = None) -> None:
    latexes: list[StringOrIO] = [data.basepath / "pdgid_to_latexname.csv"]
    if latex:
        latexes.append(latex)
    table = get_from_pdg_extended(fwf, latexes)

    with open(output, "w", newline="\n", encoding="utf-8") as f:
        f.write(version_header(output, version))
        table.to_csv(f, float_format="%.12g")


def run_regen(args: Any) -> None:
    main(args.version, args.year)


def run_convert(args: Any) -> None:
    convert(args.version, args.output, args.fwf, args.latex)


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(help="Options (pick one)")
    subparsers.required = True
    subparsers.dest = "command"

    parser_regen = subparsers.add_parser(
        "regenerate", help="Regenerate the built in files from the built in names"
    )
    parser_regen.add_argument(
        "year", help="Year of file to read in/produce (2008 is always read/produced)"
    )
    parser_regen.add_argument(
        "version", help="Version of package CSV data files to be written in headers"
    )
    parser_regen.set_defaults(func=run_regen)

    parser_convert = subparsers.add_parser(
        "extended", help="Make a new file from extended inputs"
    )
    parser_convert.add_argument("output", help="Output file name")
    parser_convert.add_argument("fwf", help="Fixed width format extended file")
    parser_convert.add_argument(
        "version", help="Version of package CSV data files to be written in headers"
    )
    parser_convert.add_argument(
        "latex",
        type=FileType("r"),
        help="Optional Latex file with names",
        nargs="?",
        default=None,
    )
    parser_convert.set_defaults(func=run_convert)

    args_ = parser.parse_args()
    args_.func(args_)
