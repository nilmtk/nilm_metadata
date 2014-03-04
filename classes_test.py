from __future__ import print_function, division
import json
from jsonschema import validate

def merge_dicts(old, new):
    """Recursively extends lists in old with lists in new,
    and updates dicts.
    
    Arguments
    ---------
    old, new : dict

    Returns
    -------
    merged : dict
    """
    merged = old.copy()
    for key, new_value in new.iteritems():
        if isinstance(new_value, list):
            try:
                merged[key].extend(new_value)
            except KeyError:
                merged[key] = new_value 

        elif isinstance(new_value, dict):
            try:
                updated_value = merged[key]
            except KeyError:
                merged[key] = new_value
            else:
                merge_dicts(updated_value, new_value)

        else:
            merged[key] = new_value
    return merged


def get_complete_class(class_name):
    classes = json.load(open('classes/appliance_classes.json'))
    subclass = classes[class_name]
    complete = subclass.copy()

    while complete.get('subtype_of'):
        parent = classes[complete['subtype_of']]
        complete = merge_dicts(complete, parent)
        if parent.get('subtype_of') is None:
            del complete['subtype_of'] 

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



for class_name in ['Refrigeration', 'Computer']:
    print("Validating", class_name)
    cls, properties = get_complete_class(class_name)
    validate_complete_class(cls, properties)
print('done validation')
