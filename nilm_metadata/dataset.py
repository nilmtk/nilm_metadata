from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors
from file_management import get_schema_directory

def concatenate_complete_dataset(dataset_obj):
    # propagate geo_location and timezone to each building
    tz = dataset_obj.get('timezone')
    geo = dataset_obj.get('geo_location')
    
    complete_dataset = dataset_obj.copy()
    buildings = complete_dataset.get('buildings', {})
    for building_id, building in buildings.iteritems():
        if tz and building.get('timezone') is None:
            building['timezone'] = tz
        if geo and building.get('geo_location') is None:
            building['geo_location'] = geo

        # TODO:
        # building = concatenate_complete_building(building)
        
        buildings[building_id] = building

    return complete_dataset


def validate_complete_dataset(complete_dataset):
    schema_filename = join(get_schema_directory(), 'dataset.json')
    schema = json.load(open(schema_filename))
    validate(complete_dataset, schema)
    
    # TODO: validate each building???
    # components = complete_appliance.get('components', {})
    # for component_obj in components.values():
    #     validate_complete_appliance(component_obj)


