# Copyright (c) 2018-2024, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from typing import IO, Any, Protocol, Union, runtime_checkable

from ._compat.typing import Traversable

__all__ = (
    "StringOrIO",
    "HasOpen",
    "HasRead",
)


StringOrIO = Union[Traversable, IO[str], str]


@runtime_checkable
class HasOpen(Protocol):
    def open(self) -> Any:
        pass


@runtime_checkable
class HasRead(Protocol):
    def read(self) -> str:
        pass
