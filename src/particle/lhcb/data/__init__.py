# Copyright (c) 2018-2022, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import sys

if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    import importlib.resources as resources


basepath = resources.files(__name__)
