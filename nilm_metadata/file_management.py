from __future__ import print_function, division
from inspect import currentframe, getfile, getsourcefile
from os.path import dirname, join, isdir, isfile, getmtime, walk, basename, abspath
from os import getcwd
from sys import getfilesystemencoding
import yaml


def get_module_directory():
    # Taken from http://stackoverflow.com/a/6098238/732596
    path_to_this_file = dirname(getfile(currentframe()))
    if not isdir(path_to_this_file):
        encoding = getfilesystemencoding()
        path_to_this_file = dirname(unicode(__file__, encoding))
    if not isdir(path_to_this_file):
        abspath(getsourcefile(lambda _: None))
    if not isdir(path_to_this_file):
        path_to_this_file = getcwd()
    assert isdir(path_to_this_file), path_to_this_file + ' is not a directory'
    return path_to_this_file


def _path_to_directory(*args):
    path_to_directory = join(get_module_directory(), *args)
    assert isdir(path_to_directory)
    return path_to_directory


def get_objects_directory():
    return _path_to_directory('..', 'objects')


def get_schema_directory():
    return _path_to_directory('..', 'schema')


def find_all_files_with_suffix(suffix, directory):
    # Find all files with suffix, recursively.
    accumulator = []
    def select_object_files(accumulator, dirname, fnames):
        new_files = [join(dirname, fname) for fname in fnames 
                     if fname.endswith(suffix)]
        accumulator.extend(new_files)
        fnames = filter(lambda fname: fname != '.git', fnames)

    walk(directory, select_object_files, accumulator)
    return accumulator

    
def find_all_object_files():
    filenames = find_all_files_with_suffix('.yaml', get_objects_directory())
    filenames = filter(lambda fname: basename(fname) != 'index.yaml', filenames)
    return filenames


def get_object_cache():
    obj_filenames = find_all_object_files()
    obj_cache = {}
    for filename in obj_filenames:
        with open(filename) as fh:
            objs = yaml.load(fh)
        obj_cache.update(objs)

    return obj_cache
