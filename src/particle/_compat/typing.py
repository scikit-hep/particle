# Copyright (c) 2018-2024, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

import sys

if sys.version_info < (3, 9):
    from importlib_resources.abc import Traversable
elif sys.version_info < (3, 11):
    from importlib.abc import Traversable
else:
    from importlib.resources.abc import Traversable


__all__ = ("Traversable",)
