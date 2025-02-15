from nilm_metadata.object_concatenation import get_appliance_types, recursively_update_dict
from nilm_metadata.convert_yaml_to_hdf5 import convert_yaml_to_hdf5, save_yaml_to_datastore

import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'central_metadata', path)
