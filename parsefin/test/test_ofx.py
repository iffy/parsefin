# Copyright (c) Matt Haggard.
# See LICENSE for details.

from twisted.trial.unittest import TestCase
from datetime import datetime

from parsefin.ofx import timestamp



class timestampTest(TestCase):


    def test_millisecond(self):
        self.assertEqual(
            timestamp('20140709211711.753'),
            datetime(2014, 7, 9, 21, 17, 11, 753000))


    def test_no_millisecond(self):
        self.assertEqual(
            timestamp('20140709211711'),
            datetime(2014, 7, 9, 21, 17, 11))


    def test_timezone(self):
        """
        Should convert things to UTC.
        """
        self.assertEqual(
            timestamp('20140709021711.000[-8:PST]'),
            datetime(2014, 7, 9, 10, 17, 11))
        self.assertEqual(
            timestamp('20140709021711[-8:PST]'),
            datetime(2014, 7, 9, 10, 17, 11))
        self.assertEqual(
            timestamp('20140709[-8:PST]'),
            datetime(2014, 7, 9, 8, 0, 0))


    def test_justdate(self):
        """
        Should handle YYYYMMDD but still make a datetime
        """
        self.assertEqual(
            timestamp('20140709'),
            datetime(2014, 7, 9, 0, 0, 0))
