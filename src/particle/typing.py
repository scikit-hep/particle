# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import, division, print_function

import sys

if sys.version_info < (3, 8):
    from typing_extensions import Protocol, runtime_checkable
else:
    from typing import Protocol, runtime_checkable

from typing import Any


@runtime_checkable
class HasOpen(Protocol):
    def open(self):
        # type: () -> Any
        pass


@runtime_checkable
class HasRead(Protocol):
    def read(self):
        # type: () -> str
        pass
