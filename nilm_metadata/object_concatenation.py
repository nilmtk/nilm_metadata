from __future__ import print_function, division
import json, yaml
from file_management import map_obj_names_to_filenames


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
            if not any([isinstance(v, dict) for v in old[key]]):
                old[key] = list(set(old[key]))
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
    if object_name is None:
        return []
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
    

def concatenate_complete_object(object_name, child_object=None, 
                                do_not_inherit_extension_list=None):
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
        if '~' in next_child.get('name', ''):
            do_not_inherit.append('name')
        do_not_inherit.extend(['synonyms', 'description'])
        if do_not_inherit_extension_list:
            do_not_inherit.extend(do_not_inherit_extension_list)
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


