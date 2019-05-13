#!/usr/bin/env python
# Copyright (c) 2018-2019, Eduardo Rodrigues and Henry Schreiner.
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/scikit-hep/particle for details.

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

from setuptools import setup
from setuptools import find_packages

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

install_deps = [
    'enum34>=1.1; python_version<"3.4"',
    'importlib_resources>=1.0; python_version<"3.7"',
    'attrs>=17.4.0',
    'hepunits>=0.1.0'
]

extras = {
    'test': ['pytest', 'pandas'],
    'convert': ['pandas'],
}

def get_version():
    g = {}
    exec(open(os.path.join("particle", "_version.py")).read(), g)
    return g["__version__"]

setup(
    name = 'Particle',
    author = 'Eduardo Rodrigues',
    author_email = 'eduardo.rodrigues@cern.ch',
    maintainer = 'The Scikit-HEP admins',
    maintainer_email = 'scikit-hep-admins@googlegroups.com',
    version = get_version(),
    description = 'PDG particle data and identification codes',
    long_description = open('README.rst').read(),
    url = 'https://github.com/scikit-hep/particle',
    license = 'new BSD',
    packages = find_packages(),
    package_data={'': ['data/*.*']},
    install_requires = install_deps,
    setup_requires = [] + pytest_runner,
    tests_require = extras['test'],
    extras_require = extras,
    keywords = [
        'HEP', 'PDG', 'PDGID', 'particle', 'particle data table',
    ],
    classifiers = [
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 4 - Beta',
    ],
    platforms = "Any",
)
