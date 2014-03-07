#!/usr/bin/env python
from __future__ import print_function

from jsonschema import validate
import json, unittest, sys
from ..object_concatenation import merge_dicts

class TestObjectConcatenation(unittest.TestCase):

    def test_merge_dicts(self):
        d1 = {}
        d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
        merge_dicts(d1,d2)
        self.assertEqual(d1, d2)

        d1 = {'a':-1, 'b':-3, 'c': {}}
        d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
        merge_dicts(d1,d2)
        self.assertEqual(d1, d2)

        d1 = {'a':-1, 'b':-3, 'c': {}, 'list': [1,2,3]}
        d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20}, 'list': [4,5,6] }
        merge_dicts(d1,d2)
        self.assertEqual(d1, {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20}, 'list': [1,2,3,4,5,6] })

        d1 = {'a':-1, 'b':-3}
        d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
        merge_dicts(d1,d2)
        self.assertEqual(d1, d2)

        d1 = {'a':-1, 'b':-3, 'c': {'ca':-10, 'cc': 30} }
        d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
        merge_dicts(d1,d2)
        self.assertEqual(d1, {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20, 'cc': 30} })

if __name__ == '__main__':
    unittest.main()
