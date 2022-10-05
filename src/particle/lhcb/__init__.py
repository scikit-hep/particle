# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

from .converters import LHCbName2PDGIDBiMap
from .functions import from_lhcb_name, to_lhcb_name

__all__ = (
    "from_lhcb_name",
    "to_lhcb_name",
    "LHCbName2PDGIDBiMap",
)


def __dir__() -> tuple[str, ...]:
    return __all__
