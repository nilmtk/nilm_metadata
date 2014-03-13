from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors
from file_management import get_schema_directory
from building import concatenate_complete_building, validate_complete_buildings
from building import validate_complete_appliances, validate_complete_meters
from schema_preprocessing import local_validate


def concatenate_complete_dataset(dataset_obj, object_cache):
    # propagate geo_location and timezone to each building
    tz = dataset_obj.get('timezone')
    geo = dataset_obj.get('geo_location')
    voltage = dataset_obj.get('mains_voltage')
    
    complete_dataset = dataset_obj.copy()
    buildings = complete_dataset.get('buildings', [])
    for i, building in enumerate(buildings):
        if tz and building.get('timezone') is None:
            building['timezone'] = tz
        if geo and building.get('geo_location') is None:
            building['geo_location'] = geo

        electric = building.get('utilities', {}).get('electric', {})
        if voltage and electric and electric.get('mains_voltage') is None:
            electric['mains_voltage'] = voltage

        building = concatenate_complete_building(building, object_cache)        
        buildings[i] = building

    return complete_dataset


def validate_complete_dataset(complete_dataset):
    schema_filename = join(get_schema_directory(), 'dataset.json')
    schema = json.load(open(schema_filename))
    local_validate(complete_dataset, schema)
    
    items = complete_dataset['items']
    validation_funcs = {
        'buildings': validate_complete_buildings,
        'appliances': validate_complete_appliances,
        'meters': validate_complete_meters
    }
    objects = complete_dataset.get(items, [])
    validation_funcs[items](objects)
