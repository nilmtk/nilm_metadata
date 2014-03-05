from __future__ import print_function, division
import json
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
    classes = json.load(open('classes/appliance_classes.json'))
    subclass = classes[class_name]
    complete = subclass.copy()

    while complete.get('parent'):
        parent = classes[complete['parent']]
        merge_dicts(complete, parent)
        if parent.get('parent') is None:
            del complete['parent'] 

    try:
        properties = complete.pop('additional_properties')
    except KeyError:
        properties = {}

    return complete, properties


def validate_complete_class(complete_class, properties):
    appliance_schema = json.load(open('schema/appliance.json'))
    appliance_schema['properties'].update(properties)
    validate(complete_class, appliance_schema)
    return appliance_schema


test_merge_dicts()
for class_name in ['Refrigeration', 'Computer']:
    print("Validating", class_name)
    cls, properties = get_complete_class(class_name)
    validate_complete_class(cls, properties)
print('done validation')
