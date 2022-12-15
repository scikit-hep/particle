# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from .corsika7id import Corsika7ID

__all__ = ("Corsika7ID",)


def __dir__() -> tuple[str, ...]:
    return __all__
