# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

import sys
from typing import Any, TextIO, Union

if sys.version_info < (3, 8):
    from typing_extensions import Protocol, runtime_checkable
else:
    from typing import Protocol, runtime_checkable

if sys.version_info < (3, 9):
    from importlib_resources.abc import Traversable
else:
    from importlib.abc import Traversable


__all__ = (
    "Protocol",
    "runtime_checkable",
    "Traversable",
    "StringOrIO",
    "HasOpen",
    "HasRead",
)


StringOrIO = Union[Traversable, str, TextIO]


@runtime_checkable
class HasOpen(Protocol):
    def open(self) -> Any:
        pass


@runtime_checkable
class HasRead(Protocol):
    def read(self) -> str:
        pass
