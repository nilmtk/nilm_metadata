from __future__ import print_function, division
import json
from jsonschema import validate, ValidationError
from os.path import join

from object_concatenation import concatenate_complete_object, get_ancestors
from file_management import get_schema_directory

def concatenate_complete_appliance(appliance_obj):
    parent_name = appliance_obj['parent']
    complete_appliance = concatenate_complete_object(parent_name, appliance_obj).copy()

    ##############################
    # Check components_set are valid
    all_allowed_components = complete_appliance.get('all_allowed_components', [])
    all_allowed_components = set(all_allowed_components)
    components = complete_appliance.get('components', {})
    components_set = set(components.keys())
    if not components_set.issubset(all_allowed_components):
        incorrect_components = components_set - all_allowed_components
        # For each incorrect component, check to see if it is a 
        # child of an allowed component
        for c in incorrect_components:
            ancestors = get_ancestors(c)
            ancestors = [a['name'] for a in ancestors]
            if not any([ancestor in all_allowed_components
                        for ancestor in ancestors]):
                msg = ('Components ' + c + ' nor any of its ancestors'
                       ' are allowed for appliance ' + parent_name)
                raise ValidationError(msg)

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
    for component_name, component_obj in components.iteritems():
        component_obj = concatenate_complete_appliance(component_obj)
        components[component_name] = component_obj
        complete_appliance['categories'].update(component_obj.get('categories', {}))

    return complete_appliance


def validate_complete_appliance(complete_appliance):
    try:
        additional_properties = complete_appliance.pop('additional_properties')
    except KeyError:
        additional_properties = {}
    schema_filename = join(get_schema_directory(), 'appliance.json')
    appliance_schema = json.load(open(schema_filename))
    appliance_schema['properties'].update(additional_properties)
    validate(complete_appliance, appliance_schema)
    
    # now validate each component recursively
    components = complete_appliance.get('components', {})
    for component_obj in components.values():
        validate_complete_appliance(component_obj)
