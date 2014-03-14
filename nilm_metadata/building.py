from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors
from file_management import get_schema_directory
from appliance import concatenate_complete_appliance, validate_complete_appliance
from schema_preprocessing import combine, local_validate


def get_electric(building_obj):
    return building_obj.get('utilities', {}).get('electric', {})    


def get_appliances(building_obj):
    return get_electric(building_obj).get('appliances', [])


def get_meters(building_obj):
    return get_electric(building_obj).get('meters', [])


def concatenate_complete_building(building_obj, object_cache):
    complete_building = building_obj.copy()
    appliances = get_appliances(complete_building)
    for i, appliance_obj in enumerate(appliances):
        appliances[i] = concatenate_complete_appliance(appliance_obj, object_cache)

    meters = get_meters(complete_building)
    for i, meter_obj in enumerate(meters):
        meters[i] = concatenate_complete_object(meter_obj['parent'], 
                                                object_cache,
                                                child_object=meter_obj,
                                                do_not_inherit_extension_list=['name'])

    return complete_building


def validate_complete_buildings(buildings):
    # Validate each building
    for building_obj in buildings:
        validate_complete_building(building_obj)


def validate_complete_building(complete_building):
    schema_filename = join(get_schema_directory(), 'building.json')
    schema = json.load(open(schema_filename))
    local_validate(complete_building, schema)

    validate_complete_meters(get_meters(complete_building))
    validate_complete_appliances(get_appliances(complete_building))


def validate_complete_meters(meters):
    # Validate each meter separately because we need to combine
    # 'device' and 'meter' together using combine
    # This won't be necessary if JSON-Schema draft 5 includes
    # a mechanism to forbid extra properties even when
    # using 'allOf'
    meter_schema_filename = join(get_schema_directory(), 'meter.json')
    meter_schema = json.load(open(meter_schema_filename))
    combine(meter_schema)
    for meter_obj in meters:
        local_validate(meter_obj, meter_schema)


def validate_complete_appliances(appliances):
    # Validate each appliance (because we insert additional properties
    # so validation cannot be done without some schema pre-processing)
    appliance_ids = [] # name and instance
    for appliance_obj in appliances:
        validate_complete_appliance(appliance_obj)
        try:
            appliance_id = (appliance_obj['name'], appliance_obj['instance'])
        except KeyError as e:
            raise KeyError("problem with '" + appliance_obj.get('name') + "': " +
                           "KeyError:" + str(e))
            
        if appliance_id in appliance_ids:
            raise ValidationError("multiple appliances names with the same"
                                  " instance number! For appliance '{}'!"
                                  .format(appliance_id))
        else:
            appliance_ids.append(appliance_id)

