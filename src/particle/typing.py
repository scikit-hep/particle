# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from importlib.resources.abc import Traversable
from typing import IO, Any, Protocol, Self, runtime_checkable

__all__ = (
    "HasOpen",
    "HasRead",
    "Self",
    "StringOrIO",
    "Traversable",
)


StringOrIO = Traversable | IO[str] | str


@runtime_checkable
class HasOpen(Protocol):
    def open(self) -> Any:
        pass


@runtime_checkable
class HasRead(Protocol):
    def read(self) -> str:
        pass
