# Copyright (c) Matt Haggard.
# See LICENSE for details.

from setuptools import setup, find_packages

import os, re

root_dir = os.path.dirname(os.path.abspath(__file__))

def getVersion():
    r_version = re.compile(r'__version__\s*=\s*"(.*?)"')
    version_file = os.path.join(root_dir, 'parsefin/version.py')
    guts = open(version_file, 'r').read()
    m = r_version.search(guts)
    if not m:
        raise Exception("Could not find version information")
    return m.groups()[0]


setup(
    url='https://github.com/iffy/parsefin',
    author='Matt Haggard',
    author_email='haggardii@gmail.com',
    name='parsefin',
    version=getVersion(),
    packages=find_packages(),
    scripts=[
        'scripts/parsefin',
    ],
    install_requires=[
        "lxml",
        "pytz",
    ],
)
