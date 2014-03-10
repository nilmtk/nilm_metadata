#!/usr/bin/env python
from __future__ import print_function

try:
    from jsonschema import validate
except ImportError as er:
    msg = str(er) + "\n"
    msg += "Please install 'jsonschema' using 'pip install jsonschema'"
    raise ImportError(msg)

import json, unittest, sys
from os.path import walk, join
from ..file_management import get_schema_directory, get_module_directory
from ..appliance import concatenate_complete_appliance, validate_complete_appliance
from ..dataset import concatenate_complete_dataset, validate_complete_dataset
from ..building import concatenate_complete_building, validate_complete_building
import yaml

def examples_directory():
    return join(get_module_directory(), '..', 'examples')

class TestSchema(unittest.TestCase):

    def test_json(self):
        """Check that all JSON files are valid JSON."""

        # Find json files
        json_files = []
        def select_json_files(json_files, dirname, fnames):
            new_json_files = [join(dirname, fname) for fname in fnames 
                              if fname.endswith('.json')]
            json_files.extend(new_json_files)
            fnames = filter(lambda fname: fname != '.git', fnames)

        walk(get_schema_directory(), select_json_files, json_files)
        print("Found", len(json_files), "JSON files..."
              " will now test they are valid JSON... ", end="")

        # Test json files
        for json_file in json_files:
            try:
                json.load(open(json_file))
            except:
                print('Error loading ', json_file, file=sys.stderr)
                raise
        print("done and all are OK!")

    def test_appliance_group(self):
        appliances = yaml.load(open(join(examples_directory(), 
                                         'appliance_group.yaml')))
        complete_appliance = concatenate_complete_appliance(appliances['light,1'])
#        print(json.dumps(complete_appliance, indent=4))
        validate_complete_appliance(complete_appliance)
        self.assertFalse(complete_appliance.get('synonyms'))
        self.assertFalse(complete_appliance.get('description'))
        print('done validation')
        

    def test_building(self):
        dataset = yaml.load(open(join(examples_directory(), 
                                         'dataset.yaml')))
        building = dataset['buildings'][1]
        complete_building = concatenate_complete_building(building)
        print(json.dumps(complete_building, indent=4))
        validate_complete_building(complete_building)

    def test_dataset(self):
        dataset = yaml.load(open(join(examples_directory(), 
                                         'dataset.yaml')))
        complete_dataset = concatenate_complete_dataset(dataset)
#        print(json.dumps(complete_dataset, indent=4))
        self.assertEqual(complete_dataset['buildings'][1]['timezone'], 
                         'Europe/London')
        validate_complete_dataset(complete_dataset)



if __name__ == '__main__':
    unittest.main()
