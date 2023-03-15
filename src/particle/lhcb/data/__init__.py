# Copyright (c) 2018-2023, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import sys

if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    from importlib import resources


__all__ = ("basepath",)


basepath = resources.files(__name__)


def __dir__() -> tuple[str, ...]:
    return __all__
