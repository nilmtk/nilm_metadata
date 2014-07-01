from __future__ import print_function, division
import yaml
import pandas as pd
from os.path import isdir, isfile, join, splitext
from os import listdir
from sys import stderr

"""
TODO:

Do sanity checks (make sure there aren't multiple appliance types with same 
instance, or no instance 1).  Make sure we use proper NILM Metadata names.
"""

def convert_yaml_to_hdf5(yaml_dir, hdf_filename):
    assert isdir(yaml_dir)
    store = pd.HDFStore(hdf_filename, 'a')

    # Load Dataset and MeterDevice metadata
    metadata = _load_file(yaml_dir, 'dataset.yaml')
    metadata['meter_devices'] = _load_file(yaml_dir, 'meter_devices.yaml')
    store.root._v_attrs.metadata = metadata

    # Load buildings
    building_filenames = [fname for fname in listdir(yaml_dir)
                          if fname.startswith('building') 
                          and fname.endswith('.yaml')]

    for fname in building_filenames:
        building = splitext(fname)[0] # e.g. 'building1'
        group = store._handle.create_group('/', building)
        group._f_setattr('metadata', _load_file(yaml_dir, fname))

    store.close()
    print("Done!")

def _load_file(yaml_dir, yaml_filename):
    yaml_full_filename = join(yaml_dir, yaml_filename)
    if isfile(yaml_full_filename):
        with open(yaml_full_filename) as fh:
            return yaml.load(fh)
    else:
        print(yaml_full_filename, "not found.", file=stderr)
