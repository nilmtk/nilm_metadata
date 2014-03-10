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
    # Find all YAML files
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


def map_obj_names_to_filenames():
    PATH_TO_OBJECTS = get_objects_directory()
    INDEX_FILENAME = join(PATH_TO_OBJECTS, 'index.yaml')
    OBJECT_FILENAMES = find_all_object_files()

    # check if cache file exists
    if isfile(INDEX_FILENAME):
        # check if any of the object files are younger than the index
        mtime_for_index = getmtime(INDEX_FILENAME)
        regenerate_index = False
        for fname in OBJECT_FILENAMES:
            mtime = getmtime(fname)
            if mtime >= mtime_for_index:
                regenerate_index = True
                break
    else:
        regenerate_index = True

    if regenerate_index:
        index_dict = {}
        for fname in OBJECT_FILENAMES:
            objects = yaml.load(open(fname))
            if not objects:
                continue
            index_dict.update({k:fname for k in objects.keys()})

        # Make the filenames relative for caching to disk
        index_dict_relative = {k:v.replace(PATH_TO_OBJECTS, '')[1:]
                               for k,v in index_dict.iteritems()}
        with open(INDEX_FILENAME, 'w') as fh:
            yaml.dump(index_dict_relative, fh, default_flow_style=False)
    else:
        with open(INDEX_FILENAME, 'r') as fh:
            index_dict_relative = yaml.load(fh)
        index_dict = {k:join(PATH_TO_OBJECTS,v) 
                      for k,v in index_dict_relative.iteritems()}

    return index_dict
