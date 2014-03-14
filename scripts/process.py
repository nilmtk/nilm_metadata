#!/usr/bin/env python
from __future__ import print_function, division
from nilm_metadata.dataset import (concatenate_complete_dataset, 
                                   validate_complete_dataset)
import argparse, yaml, json
from sys import stderr, stdout
import sys
from os.path import splitext

parser = argparse.ArgumentParser(
    description= "Concatenate and/or validate a NILM metadata.")
parser.add_argument('input', help='filename of the input YAML or JSON metadatafile')
parser.add_argument('-o', '--output', help='filename of the output YAML or JSON file',
                    default=None)
parser.add_argument('-v', '--validate_only', action='store_true')
parser.add_argument('-c', '--concatenate_only', action='store_true')
args = parser.parse_args()

# LOAD INPUT FILE
print("Loading", args.input, "... ", end="")
stdout.flush()
try:
    fh = open(args.input)
except IOError as e:
    exit('\n'+str(e).replace('[Errno 2]', 'ERROR loading input file:'))

def invalid_file_extension(pre_message, error):
    print('\n' + pre_message + str(error) + " is not a valid file extension."
          "  Should be '.json' or '.yaml'", file=stderr)

# CONVERT FROM YAML/JSON TO PYTHON DICT
input_ext = splitext(args.input)[1]
load_funcs = {'.yaml': yaml.load, '.json': json.load}
try:
    dataset = load_funcs[input_ext](fh)
except KeyError as e:
    invalid_file_extension("ERROR loading input file: ", e)
    exit(1)
print("done loading.\n")

# CONCATENATE
if not args.validate_only:
    if dataset.get('has_been_concatenated'):
        print("Dataset '" + args.input + "' has already been concatenated!"
              "  Will not concatenate again.\n")
    else:
        print("Concatenating... ", end="")
        stdout.flush()
        dataset = concatenate_complete_dataset(dataset)
        print("done concatenating.\n")
        
        # WRITE TO DISK
        if args.output is not None:
            output_ext = splitext(args.output)[1]
            dump_funcs = {'.yaml': yaml.dump, '.json': json.dump}
            print("Dumping output to", args.output, "... ", end="")
            stdout.flush()
            try:
                fh = open(args.output, 'w') 
            except IOError as e:
                print('ERROR writing output file:', str(e), file=stderr)
            else:
                try:
                    dump_funcs[output_ext](dataset, fh)
                except KeyError as e:
                    invalid_file_extension('ERROR writing output file: ', e)
                    print()
                else:
                    print("Done dumping output.\n")

# VALIDATE
if not args.concatenate_only:
    print("Validating... ", end="")
    stdout.flush()
    if dataset.get('has_been_concatenated'):
        validate_complete_dataset(dataset)
        print("done validation!  It passed!\n")
    else:
        exit("\nERROR: Cannot validate a metadata file which has not yet been concatenated!")
