#!/usr/bin/env python
from __future__ import print_function, division
from nilm_metadata.dataset import validate_complete_dataset
import argparse, yaml

parser = argparse.ArgumentParser()
#parser.add_help('Concatenate a NILM metadata file describing a NILM dataset.')
parser.add_argument('input', help='input YAML file')
args = parser.parse_args()

with open(args.input) as fh:
    print("Loading", args.input, "...")
    dataset = yaml.load(fh)
    print("    Done loading.")

print("Validating...")
validate_complete_dataset(dataset)
print("    Done validation!  It passed!")
