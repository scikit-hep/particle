from __future__ import annotations

import sys

if sys.version_info < (3, 13):
    from typing_extensions import deprecated
else:
    from warnings import deprecated

__all__ = ["deprecated"]
