from __future__ import print_function, division
import json, yaml
from jsonschema import validate

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

def test_merge_dicts():
    d1 = {}
    d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
    merge_dicts(d1,d2)
    assert d1 == d2

    d1 = {'a':-1, 'b':-3, 'c': {}}
    d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
    merge_dicts(d1,d2)
    assert d1 == d2

    d1 = {'a':-1, 'b':-3, 'c': {}, 'list': [1,2,3]}
    d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20}, 'list': [4,5,6] }
    merge_dicts(d1,d2)
    assert d1 == {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20}, 'list': [1,2,3,4,5,6] }

    d1 = {'a':-1, 'b':-3}
    d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
    merge_dicts(d1,d2)
    assert d1 == d2

    d1 = {'a':-1, 'b':-3, 'c': {'ca':-10, 'cc': 30} }
    d2 = {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20} }
    merge_dicts(d1,d2)
    assert d1 == {'a':1, 'b':2, 'c': {'ca':10, 'cb': 20, 'cc': 30} }


def get_complete_class(class_name):
    classes = yaml.load(open('appliances/lights.yaml'))

    # walk the inheritance tree from 
    # most-derived class upwards (which is the wrong direction
    # for actually doing inheritance)
    class_list = [class_name]
    current_class = classes[class_name]
    while current_class.get('parent'):
        parent_name = current_class['parent']
        class_list.append(parent_name)
        current_class = classes[parent_name]

    # Now descend from super-class downwards,
    # collecting and updating properties as we go.
    class_list.reverse()
    merged_class = classes[class_list[0]].copy()
    for class_name in class_list[1:]:
        merge_dicts(merged_class, classes[class_name])

    for property_to_remove in ['parent', 'description']:
        del merged_class[property_to_remove]

    try:
        properties = merged_class.pop('additional_properties')
    except KeyError:
        properties = {}

    return merged_class, properties

def validate_complete_appliance(complete_appliance, additional_properties):
    appliance_schema = json.load(open('schema/appliance.json'))
    appliance_schema['properties'].update(additional_properties)
    validate(complete_appliance, appliance_schema)
    return appliance_schema

def get_complete_appliance(appliance):
    appliance_class_name = appliance['class']
    cls, properties = get_complete_class(appliance_class_name)
    complete_appliance = cls.copy()
    complete_appliance.update(appliance)
    print(json.dumps(complete_appliance, indent=4))

    # Merge components
    default_components = cls.get('default_components', {})
    components = default_components.copy()
    components.update(appliance.get('components', {}))

    # Check components are valid
    additional_components_allowed = cls.get('additional_components_allowed',{})
    all_allowed_components = (set(default_components.keys())
                              .union(set(additional_components_allowed.keys())))

    if not set(components.keys()).issubset(all_allowed_components):
        incorrect_components = set(components.keys()) - all_allowed_components
        raise KeyError(str(list(incorrect_components)) + ' are not allowed for '
                       + appliance_class_name)
    else:
        complete_appliance['components'] = components

    for property_to_remove in [
            'types', 'default_components', 
            'additional_components_allowed']:
        del complete_appliance[property_to_remove]
    print(json.dumps(complete_appliance, indent=4))
    return complete_appliance, properties

test_merge_dicts()
appliances = yaml.load(open('appliances/lights.yaml'))['test_appliance_group']
complete_appliance, additional_properties = get_complete_appliance(appliances['light,1'])
# validate_complete_appliance(complete_appliance, additional_properties)
print('done validation')

