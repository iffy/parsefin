# Copyright (c) Matt Haggard.
# See LICENSE for details.

from distutils.core import setup
from pip.req import parse_requirements

import os, re


def getVersion():
    r_version = re.compile(r'__version__\s*=\s*"(.*?)"')
    version_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parsefin/version.py')
    guts = open(version_file, 'r').read()
    m = r_version.search(guts)
    if not m:
        raise Exception("Could not find version information")
    return m.groups()[0]


def parseRequirements():
    reqs = parse_requirements('requirements.txt')
    packages = []
    links = []
    for req in reqs:
        if req.url:
            links.append(str(req.url))
            packages.append(str(req.req))
        else:
            packages.append(str(req.req))
    return packages, links

install_requires, dependency_links = parseRequirements()


setup(
    url='https://github.com/iffy/parsefin',
    author='Matt Haggard',
    author_email='haggardii@gmail.com',
    name='parsefin',
    version=getVersion(),
    packages=[
        'parsefin', 'parsefin.test',
    ],
    scripts=[
        'bin/parsefin',
    ],
    install_requires=install_requires,
    dependency_links=dependency_links,
)
