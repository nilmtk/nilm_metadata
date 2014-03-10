from __future__ import print_function, division
import json, yaml
from jsonschema import validate, ValidationError
from file_management import map_obj_names_to_filenames, get_schema_directory, get_module_directory
from os.path import join

def merge_dicts(old, new):
    """ Recursively extends lists in old with lists in new,
    and updates dicts.    

    Arguments
    ---------
    old, new : dict
        Updates `old` in place.
    """
    for key, new_value in new.iteritems():
        if isinstance(new_value, list):
            old.setdefault(key, []).extend(new_value)
        elif isinstance(new_value, dict):
            merge_dicts(old.setdefault(key, {}), new_value)
        else:
            old[key] = new_value


def get_ancestors(object_name):
    """
    Arguments
    ---------
    object_name: string
    
    Returns
    -------
    A list of dicts where each dict is an object. The first
    dict is the highest on the inheritance hierarchy; the last dict
    is the object with name == `object_name`.
    """
    object_filenames = map_obj_names_to_filenames()
    name_of_file_containing_object = object_filenames[object_name]
    yaml_file = yaml.load(open(name_of_file_containing_object))

    # walk the inheritance tree from 
    # bottom upwards (which is the wrong direction
    # for actually doing inheritance)
    current_object = yaml_file[object_name]
    current_object['name'] = object_name
    ancestors = [current_object]
    while current_object.get('parent'):
        parent_name = current_object['parent']
        name_of_file_containing_parent = object_filenames[parent_name]
        if name_of_file_containing_object != name_of_file_containing_parent:
            name_of_file_containing_object = name_of_file_containing_parent
            yaml_file = yaml.load(open(name_of_file_containing_object))

        current_object = yaml_file[parent_name]
        current_object['name'] = parent_name
        ancestors.append(current_object)

    ancestors.reverse()
    return ancestors
    

def concatenate_complete_object(object_name, child_object=None):
    """
    Returns
    -------
    merged_object: dict.  
        If `child_object` is None then merged_object will be the object
        identified by `object_name` merged with its ancestor tree.
        If `child_object` is not None then it will be merged as the 
        most-derived object (i.e. a child of object_name).  This is 
        useful for appliances.
    """
    ancestors = get_ancestors(object_name)
    if child_object:
        ancestors.append(child_object)

    n_ancestors = len(ancestors)

    # Now descend from super-object downwards,
    # collecting and updating properties as we go.
    merged_object = ancestors[0].copy()
    for i, next_child in enumerate(ancestors[1:]):
        # Remove properties that the child does not want to inherit
        do_not_inherit = next_child.get('do_not_inherit', [])
        do_not_inherit.extend(['synonyms', 'description'])
        for property_to_not_inherit in do_not_inherit:
            try:
                merged_object.pop(property_to_not_inherit)
            except KeyError:
                pass
        
        # for parameter in merged_object.get('distributions', {}).values():
        #     for dist in parameter:
        #         dist['ancestor'] = n_ancestors - i
        #         print(dist)

        merge_dicts(merged_object, next_child)

    return merged_object


def concatenate_complete_appliance(appliance_obj, parent_name):
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
        component_obj = concatenate_complete_appliance(component_obj, 
                                                       component_name)
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


