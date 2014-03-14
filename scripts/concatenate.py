#!/usr/bin/env python
from __future__ import print_function, division
from nilm_metadata.dataset import concatenate_complete_dataset
import argparse, yaml

parser = argparse.ArgumentParser()
#parser.add_help('Concatenate a NILM metadata file describing a NILM dataset.')
parser.add_argument('input', help='input YAML file')
parser.add_argument('output', help='output YAML file')
args = parser.parse_args()

with open(args.input) as fh:
    print("Loading", args.input, "...")
    dataset = yaml.load(fh)
    print("    Done loading.")

if dataset.get('has_been_concatenated'):
    print("Dataset '" + args.input + "' has already been concatenated!  Nothing to do.")
    exit(0)

print("Concatenating...")
dataset = concatenate_complete_dataset(dataset)
print("    Done concatenating.")

print("Dumping output to", args.output, "...")
with open(args.output, 'w') as fh:
    yaml.dump(dataset, fh)
print("    Done dumping output.")
