#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

from __future__ import absolute_import
from __future__ import print_function

import os.path

from setuptools import setup
from setuptools import find_packages
from setuputils import read


def get_version():
    g = {}
    exec(open(os.path.join("hepparticle", "version.py")).read(), g)
    return g["__version__"]

setup(
    name = 'hepparticle',
    author = 'Eduardo Rodrigues',
    author_email = 'eduardo.rodrigues@cern.ch',
    maintainer = 'Eduardo Rodrigues',
    maintainer_email = 'eduardo.rodrigues@cern.ch',
    version = get_version(),
    description = 'Utilities to deal with PDG data tables and particle IDs',
    long_description = read('README.rst'),
    url = 'https://github.com/eduardo-rodrigues/hepparticle',
    license = 'new BSD',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    keywords = [
        'HEP', 'PDG', 'PDGID', 'particle',
    ],
    classifiers = [
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Topic :: Scientific/Engineering :: Physics'
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
