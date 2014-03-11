from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors
from file_management import get_schema_directory
from appliance import concatenate_complete_appliance, validate_complete_appliance


def get_electric(building_obj):
    return building_obj.get('utilities', {}).get('electric', {})    

def get_appliances(building_obj):
    return get_electric(building_obj).get('appliances', [])

def get_meters(building_obj):
    return get_electric(building_obj).get('meters', [])

def concatenate_complete_building(building_obj):
    complete_building = building_obj.copy()
    appliances = get_appliances(complete_building)
    for i, appliance_obj in enumerate(appliances):
        appliances[i] = concatenate_complete_appliance(appliance_obj)

    meters = get_meters(complete_building)
    for i, meter_obj in enumerate(meters):
        meters[i] = concatenate_complete_object(meter_obj['parent'], 
                                                meter_obj,
                                                do_not_inherit_extension_list=['name'])

    return complete_building


def validate_complete_building(complete_building):
    schema_filename = join(get_schema_directory(), 'building.json')
    schema = json.load(open(schema_filename))
    validate(complete_building, schema)

    # Validate each appliance (because we insert additional properties
    # so validation cannot be done without some schema pre-processing)
    for appliance_obj in get_appliances(complete_building):
        validate_complete_appliance(appliance_obj)

