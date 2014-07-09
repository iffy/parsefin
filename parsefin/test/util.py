# Copyright (c) Matt Haggard.
# See LICENSE for details.

import json

from twisted.python.filepath import FilePath
from parsefin import parseFile


root = FilePath(__file__).parent()


def testFile(testcase, input_filename, output_filename):
    """
    Test that a given input file produces the given output.

    @param testcase: A C{TestCase} instance.
    @param input_filename: Name of file with financial data in it.
    @param output_filename: Name of file with expected JSON output in it.
    """
    input_filename = root.preauthChild(input_filename).path
    output_filename = root.preauthChild(output_filename).path
    i_fh = open(input_filename, 'rb')
    expected = json.load(open(output_filename, 'rb'))
    actual = parseFile(i_fh)
    testcase.assertEqual(expected, actual,
        "Expected output\n%s\n\nactual:\n%s\n" % (
            json.dumps(expected, indent=2),
            json.dumps(actual, indent=2),
        ))

