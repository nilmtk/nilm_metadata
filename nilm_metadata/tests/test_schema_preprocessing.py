#!/usr/bin/env python
from __future__ import print_function

import unittest, yaml, jsonschema
from ..schema_preprocessing import combine

class TestCombine(unittest.TestCase):
    def test_combine(self):
        schema = {
            "type": "object",
            "allOf": [
                { "type": "object",
                  "properties": {
                      "foo": { "type": "object" },
                      "bar": { "type": "object" }
                    }
                },
                { "type": "object",
                  "properties": {
                      "baz": { "type": "object" },
                      "bar": { "type": "object" }
                    }
                }                
            ]
        }

        combine(schema)
        
        correct_schema = {
            "type": "object",
            "properties": {
                "foo": { "type": "object" },
                "baz": { "type": "object" },
                "bar": { "type": "object" }
            },
            "additionalProperties": False
        }

        self.assertEqual(schema, correct_schema)

    def test_resolve(self):

        schema = {
            "type": "object",
            "allOf": [
                { "$ref": "#/one" },
                { "type": "object",
                  "properties": {
                      "baz": { "type": "object" },
                      "bar": { "type": "object" }
                  }
                }                
            ],
            "one": { 
                "type": "object",
                "properties": {
                    "foo": { "type": "object" },
                    "bar": { "type": "object" }
                }
            }
        }

        correct_schema = {
            "type": "object",
            "properties": {
                "foo": { "type": "object" },
                "baz": { "type": "object" },
                "bar": { "type": "object" }
            },
            "additionalProperties": False,
            "one": { 
                "type": "object",
                "properties": {
                    "foo": { "type": "object" },
                    "bar": { "type": "object" }
                }
            }
        }

        combine(schema)
        self.assertEqual(schema, correct_schema)

if __name__ == '__main__':
    unittest.main()
