# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from .geant3id import Geant3ID

__all__ = ("Geant3ID",)


def __dir__() -> tuple[str, ...]:
    return __all__
