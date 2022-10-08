# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

import contextlib
import csv
import sys
from collections.abc import Mapping
from typing import Any, Callable, Generic, Iterator, TextIO, TypeVar, Union, overload

from .. import data
from ..exceptions import MatchingIDNotFound
from ..typing import HasOpen, HasRead, StringOrIO

A = TypeVar("A")
B = TypeVar("B")
A_conv = Callable[[str], Union[A, int]]
B_conv = Callable[[str], Union[B, int]]


class BiMap(Generic[A, B]):
    def __init__(
        self,
        class_A: type[A],
        class_B: type[B],
        converters: tuple[A_conv, B_conv] = (int, int),  # type: ignore[type-arg]
        filename: StringOrIO | None = None,
    ) -> None:
        """
        Bi-bidirectional map class.

        Parameters
        ----------
        class_A, class_B: class types
            Input class types.
        converters: tuple, optional, default=(int,int)
            Converter functions applied on each entry (row) of the file
            providing the class_a-class_B matches.
            The order of the list elements must agree with that of the classes
            passed in in the constructor.
            By default, data on the file is assumed to be integers,
            which is the typical case for PDG IDs and alike.
        filename: string or file object, optional,
                  default='<class_B_name>_to_<class_A_name>.csv',
                  where the names are taken as lowercase.
            Specify a file from which to read all class_a-class_B matches.
            It does not matter whether the file contains the input as
            val_A,val_B or val_B,val_A.

        Examples
        --------
        >>> from particle import PDGID, PythiaID

        Basic/standard usage:
        >>> bimap = BiMap(PDGID, PythiaID)

        >>> bimap[PDGID(9010221)]
        <PythiaID: 10221>
        >>> bimap[PythiaID(10221)]
        <PDGID: 9010221>

        Advanced usage:
        >>> # Either pass a file name or a file object
        >>> from particle import data
        >>> filename = data.basepath / "pdgid_to_pythiaid.csv"
        >>> bimap = BiMap(PDGID, PythiaID, filename=filename)
        """

        self.class_A: type[A] = class_A
        self.class_B: type[B] = class_B

        name_A = self.class_A.__name__.upper()
        name_B = self.class_B.__name__.upper()

        file_object: TextIO
        if filename is None:
            filename = f"{name_A.lower()}_to_{name_B.lower()}.csv"
            file_object = data.basepath.joinpath(filename).open()
        elif isinstance(filename, HasRead):
            file_object = filename
        elif isinstance(filename, HasOpen):
            file_object = filename.open()
        else:
            file_object = open(filename, encoding="utf_8")  # type: ignore[arg-type]

        with file_object as _f:
            self._to_map = {
                converters[1](v[name_B]): converters[0](v[name_A])
                for v in csv.DictReader(line for line in _f if not line.startswith("#"))
            }
            _f.seek(0)
            self._from_map = {
                converters[0](v[name_A]): converters[1](v[name_B])
                for v in csv.DictReader(line for line in _f if not line.startswith("#"))
            }

    @overload
    def __getitem__(self, value: A) -> B:
        pass

    @overload
    def __getitem__(self, value: B) -> A:
        pass

    def __getitem__(self, value: Any) -> Any:
        if isinstance(value, self.class_B):
            with contextlib.suppress(KeyError):
                return self.class_A(self._to_map[value])  # type: ignore[call-arg]
        elif isinstance(value, self.class_A):
            with contextlib.suppress(KeyError):
                return self.class_B(self._from_map[value])  # type: ignore[call-arg]

        name_A = self.class_A.__name__
        name_B = self.class_B.__name__
        msg = f"Matching {name_A}-{name_B} for input {value} not found !"
        raise MatchingIDNotFound(msg)

    def __repr__(self) -> str:
        name_A = self.class_A.__name__
        name_B = self.class_B.__name__

        return f"<{self.__class__.__name__}({name_A}-{name_B}): {len(self)} matches>"

    def __len__(self) -> int:
        """Returns the number of matches."""
        return len(self._to_map)


def DirectionalMaps(
    name_A: str,
    name_B: str,
    converters: tuple[Callable[[str], str], Callable[[str], str]] = (str, str),
    filename: StringOrIO | None = None,
) -> tuple[DirectionalMap, DirectionalMap]:
    """
    Directional map class providing a to and from mapping.

    Parameters
    ----------
    name_A, name_B: str
        Input names of information to be mapped.
    converters: tuple, optional, default=(str,str)
        Converter functions applied on each entry (row) of the file
        providing the name_a-name_B matches.
        The order of the list elements must agree with that of the
        object names passed in in the constructor.
        By default, data on the file is assumed to be strings,
        which is the typical case for particle names.
    filename: string or file object, optional, default='particle/data/conversions.csv'.
        Specify a file from which to read all name_a-name_B matches.
        It is assumed that the order of items in the file matches the order
        of arguments specified in the class constructor, hence val_A,val_B.

    Examples
    --------

    >>> from particle import data  # doctest: +SKIP
    >>> filename = data.basepath / "a_to_b.csv"  # doctest: +SKIP
    >>> A2BMap, B2AMap = DirectionalMaps('A', 'B', filename=filename)  # doctest: +SKIP
    """

    name_A = name_A.upper()
    name_B = name_B.upper()

    fieldnames = None
    file_object: TextIO
    if filename is None:
        file_object = data.basepath.joinpath("conversions.csv").open()
    elif isinstance(filename, HasOpen):
        file_object = filename.open()
    elif isinstance(filename, HasRead):
        file_object = filename
    else:
        file_object = open(filename, encoding="utf_8")  # type: ignore[arg-type]

    with file_object as _f:
        skipinitialspace = True

        to_map = {
            converters[1](v[name_B]): converters[0](v[name_A])
            for v in csv.DictReader(
                (line for line in _f if not line.startswith("#")),
                fieldnames=fieldnames,
                skipinitialspace=skipinitialspace,
            )
        }
        _f.seek(0)
        from_map = {
            converters[0](v[name_A]): converters[1](v[name_B])
            for v in csv.DictReader(
                (line for line in _f if not line.startswith("#")),
                fieldnames=fieldnames,
                skipinitialspace=skipinitialspace,
            )
        }

    return (
        DirectionalMap(name_A, name_B, from_map),
        DirectionalMap(name_B, name_A, to_map),
    )


if sys.version_info < (3, 9):
    StrStrMapping = Mapping
else:
    StrStrMapping = Mapping[str, str]


class DirectionalMap(StrStrMapping):
    # pylint: disable-next=redefined-builtin
    def __init__(self, name_A: str, name_B: str, map: dict[str, str]) -> None:
        """
        Directional map class providing a A -> B mapping.

        Parameters
        ----------
        name_A, name_B: str
            Input names of information to be mapped.
        map: dict
            Input mapping as a dictionary.
        """

        self.name_A = name_A.upper()
        self.name_B = name_B.upper()

        self._map = map

    def __getitem__(self, value: str) -> str:
        try:
            return self._map[value]
        except KeyError:
            msg = f"Matching {self.name_A}->{self.name_B} for input {value} not found !"
            raise MatchingIDNotFound(msg) from None

    def __iter__(self) -> Iterator[str]:
        return iter(self._map)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.name_A}->{self.name_B}): {len(self)} matches>"

    def __len__(self) -> int:
        """Returns the number of matches."""
        return len(self._map)
