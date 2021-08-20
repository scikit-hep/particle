# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import

from typing import Tuple

from .pythiaid import PythiaID

__all__ = ("PythiaID",)


def __dir__():
    # type: () -> Tuple[str, ...]
    return __all__
