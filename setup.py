#!/usr/bin/env python
# Copyright (c) 2018-2020, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

from setuptools import setup
from setuptools import find_packages


PYTHON_REQUIRES = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

needs_pytest = {"pytest", "test", "ptr"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

INSTALL_REQUIRES = [
    'enum34>=1.1; python_version<"3.4"',
    'importlib_resources>=1.0; python_version<"3.7"',
    "attrs>=17.4.0",
    "hepunits>=1.1.0",
]

extras = {"test": ["pytest", "pandas"], "convert": ["pandas"]}


def get_version():
    g = {}
    exec(open(os.path.join("particle", "_version.py")).read(), g)
    return g["__version__"]


setup(
    name="Particle",
    author="Eduardo Rodrigues",
    author_email="eduardo.rodrigues@cern.ch",
    maintainer="The Scikit-HEP admins",
    maintainer_email="scikit-hep-admins@googlegroups.com",
    version=get_version(),
    description="PDG particle data and identification codes",
    long_description=open("README.rst").read(),
    url="https://github.com/scikit-hep/particle",
    license="BSD 3-Clause License",
    packages=find_packages(),
    package_data={"": ["data/*.*"]},
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    setup_requires=[] + pytest_runner,
    tests_require=extras["test"],
    extras_require=extras,
    keywords=[
        "HEP",
        "PDG",
        "PDGID",
        "particle",
        "particle properties",
        "particle data table",
        "MC identification codes",
    ],
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
    ],
    platforms="Any",
)
