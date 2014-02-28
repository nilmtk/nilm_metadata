#!/usr/bin/env python
from __future__ import print_function

try:
    from jsonschema import validate
except ImportError as er:
    msg = str(er) + "\n"
    msg += "Please install 'jsonschema' using 'pip install jsonschema'"
    raise ImportError(msg)

import json, unittest

class TestSchema(unittest.TestCase):

    def test_appliance_group(self):
        validate(json.load(open('examples/appliance_group.json')),
                 json.load(open('schema/appliance_group.json')))

if __name__ == '__main__':
    unittest.main()
