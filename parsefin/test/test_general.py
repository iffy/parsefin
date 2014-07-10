# Copyright (c) Matt Haggard.
# See LICENSE for details.

from twisted.trial.unittest import TestCase
from datetime import datetime, date
import json

from parsefin.general import toJson



class toJsonTest(TestCase):


    def test_normal(self):
        """
        It should do normal json stuff.
        """
        self.assertEqual(
            json.dumps({'foo': 'bar'}),
            toJson({'foo': 'bar'})
        )


    def test_indent(self):
        """
        It should indent
        """
        self.assertEqual(
            json.dumps({'foo': 'bar'}, indent=4),
            toJson({'foo': 'bar'}, indent=4)
        )


    def test_date(self):
        self.assertEqual(toJson(date(2001, 1, 2)),
            '"2001-01-02"')


    def test_datetime(self):
        self.assertEqual(toJson(datetime(2001, 1, 2, 12, 3, 1)),
            '"2001-01-02T12:03:01"')
