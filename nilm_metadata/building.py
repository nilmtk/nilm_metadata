from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors
from file_management import get_schema_directory
from appliance import concatenate_complete_appliance

def concatenate_complete_building(building_obj):
    complete_building = building_obj.copy()
    appliances = complete_building.get('utilities', {}).get('electric', {}).get('appliances', {})
    for appliance_id, appliance_obj in appliances.iteritems():
        print('appliance id:', appliance_id)
        appliances[appliance_id] = concatenate_complete_appliance(appliance_obj)

    return complete_building


def validate_complete_building(complete_building):
    schema_filename = join(get_schema_directory(), 'building.json')
    schema = json.load(open(schema_filename))
    validate(complete_building, schema)

