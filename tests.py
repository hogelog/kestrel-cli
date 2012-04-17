#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: hogelog
'''

import unittest
from kestrelcli import cli
import kestrel


class Test(unittest.TestCase):

    def setUp(self):
        self.client = kestrel.Client(["127.0.0.1:22133"])

    def tearDown(self):
        self.client.close()

    def test_peek_get(self):
        self.assertTrue(self.client.delete("foo"))

        self.assertTrue(self.client.add("foo", "bar1"))
        self.assertTrue(self.client.add("foo", "bar2"))
        cli.main("tests.py get foo".split())
        self.assertEqual(self.client.peek("foo"), "bar2")
        self.assertEqual(self.client.get("foo"), "bar2")
        self.assertIsNone(self.client.get("foo"))

    def test_set_data(self):
        self.assertTrue(self.client.delete("foo"))

        cli.main("tests.py set foo -d bar111".split())

        self.assertEqual(self.client.get("foo"), "bar111")
        self.assertIsNone(self.client.get("foo"))

    def test_set_file(self):
        self.assertTrue(self.client.delete("foo"))

        cli.main("tests.py set foo -f tests.py".split())

        self.assertIsNotNone(self.client.get("foo"))
        self.assertIsNone(self.client.get("foo"))

    def test_delete(self):
        self.assertTrue(self.client.add("foo", "bar1"))
        self.assertTrue(self.client.add("foo", "bar2"))

        cli.main("tests.py delete foo".split())

        self.assertIsNone(self.client.get("foo"))

if __name__ == '__main__':
    unittest.main()
