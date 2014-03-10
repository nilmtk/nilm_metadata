from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors
from file_management import get_schema_directory
from appliance import concatenate_complete_appliance, validate_complete_appliance


def get_appliances(building_obj):
    return building_obj.get('utilities', {}).get('electric', {}).get('appliances', {})


def concatenate_complete_building(building_obj):
    complete_building = building_obj.copy()
    appliances = get_appliances(complete_building)
    for appliance_id, appliance_obj in appliances.iteritems():
        print('appliance id:', appliance_id)
        appliances[appliance_id] = concatenate_complete_appliance(appliance_obj)

    return complete_building


def validate_complete_building(complete_building):
    schema_filename = join(get_schema_directory(), 'building.json')
    schema = json.load(open(schema_filename))
    validate(complete_building, schema)

    # Validate each appliance (because we insert additional properties)
    for appliance_obj in get_appliances(complete_building).values():
        validate_complete_appliance(appliance_obj)

