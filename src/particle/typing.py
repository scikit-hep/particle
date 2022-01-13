# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


import sys

if sys.version_info < (3, 8):
    from typing_extensions import Protocol, runtime_checkable
else:
    from typing import Protocol, runtime_checkable

from importlib.abc import Traversable
from typing import Any, TextIO, Union

StringOrIO = Union[Traversable, str, TextIO]


@runtime_checkable
class HasOpen(Protocol):
    def open(self) -> Any:
        pass


@runtime_checkable
class HasRead(Protocol):
    def read(self) -> str:
        pass
