#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file for erin.
"""

import codecs
import os
import re
import sys

from setuptools import find_packages, setup

# Constants
INSTALL_REQUIRES = [
    "toml",
    "motor",
    "discord.py @ "
    "git+https://github.com/Rapptz/discord.py.git@rewrite#egg=discord.py",
    "coloredlogs",
    "verboselogs",
    "cookiecutter",
    "schema"
]

EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov',
        'pytest-runner',
        'tox'
    ],
    'docs': [
        'Sphinx',
        'sphinx_rtd_theme'
    ],
    'voice': [
        'PyNaCl==1.2.1'
    ]
}

# Variables
path_here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    # https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(path_here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


needs_sphinx = {'build_sphinx', 'upload_docs'}.intersection(sys.argv)
sphinx = ['sphinx'] if needs_sphinx else []
os.environ['SANIC_NO_UVLOOP'] = 'true'
os.environ['SANIC_NO_UJSON'] = 'true'

setup(
        version=find_version('erin', '__init__.py'),
        packages=find_packages(exclude=['docs', 'tests']),
        entry_points={
            'console_scripts': [
                'erin = erin.__main__:main'
            ]
        },
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        setup_requires=[] + sphinx,
        extras_require=EXTRAS_REQUIRE
)

if __name__ == "__main__":
    pass
