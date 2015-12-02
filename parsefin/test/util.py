# Copyright (c) Matt Haggard.
# See LICENSE for details.

import json

from twisted.python.filepath import FilePath
from parsefin import parseFile
from parsefin.general import toJson
from parsefin.error import Error
import difflib

root = FilePath(__file__).parent()


def testFile(testcase, input_filename, output_filename):
    """
    Test that a given input file produces the given output.

    @param testcase: A C{TestCase} instance.
    @param input_filename: Name of file with financial data in it.
    @param output_filename: Name of file with expected JSON output in it.  If
        the file has C{ERROR} as the first line, then an error is expected.
    """
    input_filename = root.preauthChild(input_filename).path
    output_filename = root.preauthChild(output_filename).path
    i_fh = open(input_filename, 'rb')
    
    expected_raw = open(output_filename, 'rb').read()
    first_line = expected_raw.split('\n', 1)[0]
    if first_line == 'ERROR':
        testcase.assertRaises(Error, parseFile, i_fh)
    else:
        expected = json.loads(toJson(json.loads(expected_raw)))
        actual = json.loads(toJson(parseFile(i_fh)))
        diff = difflib.unified_diff(
            [x+'\n' for x in json.dumps(expected, indent=2, sort_keys=True).split('\n')],
            [x+'\n' for x in json.dumps(actual, indent=2, sort_keys=True).split('\n')],
            )
        diff = list(diff)
        testcase.assertEqual(expected, actual,
            "Diff: %s" % (''.join(diff)))

