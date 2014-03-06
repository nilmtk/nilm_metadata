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
    complete = classes[class_name].copy()

    while complete.get('parent'):
        parent_name = complete['parent']
        parent = classes[parent_name]
        merge_dicts(complete, parent)
        if parent.get('parent') is None:
            del complete['parent'] 

    try:
        properties = complete.pop('additional_properties')
    except KeyError:
        properties = {}

    return complete, properties

def validate_complete_appliance(complete_appliance, additional_properties):
    appliance_schema = json.load(open('schema/appliance.json'))
    appliance_schema['properties'].update(additional_properties)
    validate(complete_appliance, appliance_schema)
    return appliance_schema

def get_complete_appliance(appliance):
    class_name = appliance['class']
    cls, properties = get_complete_class(class_name)
    print(cls)
    cls.update(appliance)
    for property_to_remove in [
            'types', 'default_components', 'description', 
            'additional_components_allowed']:
        del cls[property_to_remove]
    return cls, properties

test_merge_dicts()
appliances = yaml.load(open('appliances/lights.yaml'))['test_appliance_group']
complete_appliance, additional_properties = get_complete_appliance(appliances[0])
# validate_complete_appliance(complete_appliance, additional_properties)
print('done validation')

