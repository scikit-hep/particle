# Copyright (c) 2018-2026, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.


from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .evtgen import EvtGen2PDGNameMap, EvtGenName2PDGIDBiMap, PDG2EvtGenNameMap

if TYPE_CHECKING:
    from .corsika import Corsika72PDGIDBiMap
    from .geant import Geant2PDGIDBiMap
    from .pythia import Pythia2PDGIDBiMap

__all__ = (
    "Corsika72PDGIDBiMap",
    "EvtGen2PDGNameMap",
    "EvtGenName2PDGIDBiMap",
    "Geant2PDGIDBiMap",
    "PDG2EvtGenNameMap",
    "Pythia2PDGIDBiMap",
)

# The deprecated PDG-ID <-> MC-program-ID BiMaps are imported lazily: importing
# them eagerly would close an import cycle (particle.particle -> converters ->
# converters.corsika -> particle.corsika, which is still being initialised).
_LAZY_MODULES = {
    "Corsika72PDGIDBiMap": "corsika",
    "Geant2PDGIDBiMap": "geant",
    "Pythia2PDGIDBiMap": "pythia",
}


def __getattr__(name: str) -> Any:
    module_name = _LAZY_MODULES.get(name)
    if module_name is not None:
        from importlib import import_module  # pylint: disable=C0415

        module = import_module(f"{__name__}.{module_name}")
        return getattr(module, name)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def __dir__() -> tuple[str, ...]:
    return __all__
