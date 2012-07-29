#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
@author: hogelog
'''

import sys
import os
import unittest
import kestrel
from kestrelcli import cli
import shlex
from cStringIO import StringIO

queues = {}


class MockClient:
    def __init__(self, servers):
        pass

    def add(self, name, data):
        if name in queues:
            queue = queues[name]
        else:
            queue = queues[name] = []
        queue.append(data)
        return True

    def get(self, name):
        if name in queues:
            queue = queues[name]
            if len(queue) > 0:
                return queue.pop(0)
        return None

    def peek(self, name):
        if name in queues:
            queue = queues[name]
            if len(queue) > 0:
                return queue[0]
        return None

    def delete(self, name):
        if name in queues:
            del queues[name]
        return True


def main(cmdline):
    stdout = sys.stdout
    sys.stdout = StringIO()
    cli.main(shlex.split(cmdline), MockClient)
    value = sys.stdout.getvalue()
    sys.stdout = stdout
    return value


class Test(unittest.TestCase):

    def setUp(self):
        self.client = MockClient("test")

    def tearDown(self):
        pass

    def test_get(self):
        self.assertTrue(self.client.delete("foo"))
        self.assertTrue(self.client.add("foo", "data1"))
        self.assertTrue(self.client.add("foo", "data2"))
        self.assertEqual(main("test get foo"), "data1")
        self.assertEqual(main("test get foo"), "data2")
        self.assertEqual(main("test get foo"), "")

    def test_peek(self):
        self.assertTrue(self.client.delete("foo"))
        self.assertTrue(self.client.add("foo", "bar1"))
        self.assertTrue(self.client.add("foo", "bar2"))
        self.assertEqual(main("test peek foo"), "bar1")
        self.assertEqual(main("test peek foo"), "bar1")

    def test_set_data(self):
        self.assertTrue(self.client.delete("foo"))
        self.assertEqual(main("test set foo -d bar111"), "")
        self.assertEqual(main("test get foo"), "bar111")
        self.assertEqual(main("test get foo"), "")

    def test_set_file(self):
        self.assertTrue(self.client.delete("foo"))
        self.assertEqual(main("test set foo -f tests.py"), "")
        self.assertEqual(len(main("test get foo")), os.path.getsize(
            "tests.py"))
        self.assertEqual(main("test get foo"), "")

    def test_delete(self):
        self.assertTrue(self.client.add("foo", "bar1"))
        self.assertTrue(self.client.add("foo", "bar2"))
        self.assertTrue(main("test delete foo"))
        self.assertEqual(main("test get foo"), "")

if __name__ == '__main__':
    unittest.main()
