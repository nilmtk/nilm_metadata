from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors, merge_dicts
from file_management import get_schema_directory

def concatenate_complete_appliance(appliance_obj):
    parent_name = appliance_obj['parent']
    complete_appliance = concatenate_complete_object(parent_name, appliance_obj).copy()

    ########################
    # Check subtype is valid
    subtype = complete_appliance.get('subtype')
    subtypes = complete_appliance.get('subtypes')
    if subtype:
        if subtype not in subtypes:
            raise ValidationError(subtype + 
                                  ' is not a valid subtype for appliance ' +
                                  parent_name)

    ############################################
    # Remove properties not allowed in completed appliance object
    for property_to_remove in ['subtypes', 'all_allowed_components']:
        try:
            del complete_appliance[property_to_remove]
        except KeyError:
            pass

    # Instantiate components recursively
    components = complete_appliance.get('components', [])
    for i, component_obj in enumerate(components):
        component_obj = concatenate_complete_appliance(component_obj)
        components[i] = component_obj
        merge_dicts(complete_appliance['categories'], 
                    component_obj.get('categories', {}))

    return complete_appliance


def validate_complete_appliance(complete_appliance):
    try:
        additional_properties = complete_appliance.pop('additional_properties')
    except KeyError:
        additional_properties = {}
    schema_filename = join(get_schema_directory(), 'appliance.json')
    appliance_schema = json.load(open(schema_filename))
    appliance_schema['appliance']['properties'].update(additional_properties)
    validate(complete_appliance, appliance_schema)
    
    # now validate each component recursively
    components = complete_appliance.get('components', [])
    for component_obj in components:
        validate_complete_appliance(component_obj)
