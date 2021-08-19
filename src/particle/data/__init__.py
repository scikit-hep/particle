# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

import sys

from deprecated import deprecated

if sys.version_info < (3, 9):
    import importlib_resources as resources
else:
    import importlib.resources as resources


basepath = resources.files(__name__)


open_text = deprecated(version="0.16.0", reason="Use particle.data.basepath instead.")(
    resources.open_text
)
