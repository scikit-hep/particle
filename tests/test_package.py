# Copyright (c) 2018-2023, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import annotations

import particle


def test_package_import():
    assert particle is not None


def test_load_version():
    assert particle.__version__
