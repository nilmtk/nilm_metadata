from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError, RefResolver, Draft4Validator
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors, merge_dicts
from file_management import get_schema_directory
from schema_preprocessing import combine, local_validate

def concatenate_complete_appliance(appliance_obj, object_cache):
    parent_name = appliance_obj['parent']
    complete_appliance = concatenate_complete_object(parent_name, object_cache,
                                                     child_object=appliance_obj).copy()

    ########################
    # Check subtype is valid
    subtype = complete_appliance.get('subtype')
    subtypes = complete_appliance.get('subtypes')
    if subtype and subtype not in subtypes:
        raise ValidationError(subtype + 
                              ' is not a valid subtype for appliance ' +
                              parent_name)

    ############################################
    # Remove properties not allowed in completed appliance object
    for property_to_remove in ['subtypes', 'all_allowed_components']:
        complete_appliance.pop(property_to_remove, None)

    # Instantiate components recursively
    components = complete_appliance.get('components', [])
    for i, component_obj in enumerate(components):
        component_obj = concatenate_complete_appliance(component_obj, object_cache)
        components[i] = component_obj
        merge_dicts(complete_appliance['categories'], 
                    component_obj.get('categories', {}))

    return complete_appliance


def validate_complete_appliance(complete_appliance):
    # Load appliance schema and combine all 'allOf' keys
    schema_filename = join(get_schema_directory(), 'appliance.json')
    appliance_schema = json.load(open(schema_filename))
    combine(appliance_schema)

    # Update the schema with additional properties from the appliance
    additional_properties = complete_appliance.pop('additional_properties', {})
    appliance_schema['properties'].update(additional_properties)

    # Validate
    local_validate(complete_appliance, appliance_schema)
    
    # Validate each component recursively
    components = complete_appliance.get('components', [])
    for component_obj in components:
        validate_complete_appliance(component_obj)
