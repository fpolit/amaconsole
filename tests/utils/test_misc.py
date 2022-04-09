#!/usr/bin/env python3

from unittest import TestCase
from datetime import timedelta
from amaconsole.utils.misc import str2timedelta

class TestUtilsMisc(TestCase):

    def test_str2timedelta_complete_time(self):
        #import pdb; pdb.set_trace()
        stime = '1h30m5s'
        time = timedelta(hours=1, minutes=30, seconds=5)

        self.assertEqual(str2timedelta(stime), time)

    def test_str2timedelta_only_hour(self):
        stime = '11h'
        time = timedelta(hours=11)

        self.assertEqual(str2timedelta(stime), time)

    def test_str2timedelta_only_mins(self):
        stime = '30m'
        time = timedelta(minutes=30)

        self.assertEqual(str2timedelta(stime), time)

    def test_str2timedelta_only_secs(self):
        stime = '30s'
        time = timedelta(seconds=30)

        self.assertEqual(str2timedelta(stime), time)

    def test_str2timedelta_no_mins(self):
        stime = '11h30s'
        time = timedelta(hours=11, seconds=30)

        self.assertEqual(str2timedelta(stime), time)

    def test_str2timedelta_no_hours(self):
        stime = '30m15s'
        time = timedelta(minutes=30, seconds=15)

        self.assertEqual(str2timedelta(stime), time)

    def test_str2timedelta_no_secs(self):
        stime = '3h15m'
        time = timedelta(hours=3, minutes=15)

        self.assertEqual(str2timedelta(stime), time)
