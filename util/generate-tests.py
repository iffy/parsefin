# Copyright (c) Matt Haggard.
# See LICENSE for details.

#!/usr/bin/env python

from twisted.python import usage
from twisted.python.filepath import FilePath
from jinja2 import Environment

import re

r_methsafe = re.compile('[^0-9a-zA-Z_]')

TEMPLATE = '''
#======================================
# THIS FILE IS AUTOMATICALLY GENERATED
# See util/generate-tests.py
#======================================

# Copyright (c) Matt Haggard.
# See LICENSE for details.


from twisted.trial.unittest import TestCase
from parsefin.test.util import testFile


class TestFiles(TestCase):

{% for (i,o,name) in test_cases %}
    def test_{{ name }}(self):
        """
        {{ i }} -> {{ o }}
        """
        testFile(self, '{{ i }}', '{{ o }}')

{% endfor %}
'''

def methodName(name):
    name = name.replace('.','_').replace('-','_')
    return r_methsafe.sub('', name)

def relativePath(root, path):
    segments = path.segmentsFrom(root)
    return '/'.join(segments)


def generateTestFile(input_dir, output_filename, relative_root):
    root = FilePath(input_dir)
    relative_root = FilePath(relative_root)
    inputs = [relativePath(relative_root, x) for x in sorted(root.globChildren('*.input*'))]
    names = [methodName(FilePath(x).basename()) for x in inputs]
    outputs = [relativePath(relative_root, x) for x in sorted(root.globChildren('*.output*'))]
    test_cases = zip(inputs, outputs, names)

    print 'test_cases', test_cases

    env = Environment()
    template = env.from_string(TEMPLATE)
    rendered = template.render({'test_cases': test_cases})
    FilePath(output_filename).setContent(rendered)


class Options(usage.Options):

    optParameters = [
        ('output', 'o', None, "File to produce"),
        ('input', 'i', None, "Directory to read test cases from"),
        ('relative-root', 'r', None, "Directory from which files are relative"),
    ]



if __name__ == '__main__':
    options = Options()
    options.parseOptions()
    output = generateTestFile(options['input'], options['output'],
        options['relative-root'])
