from __future__ import print_function, division
from inspect import currentframe, getfile
from os.path import dirname, join, isdir, isfile, getmtime, walk
import yaml


def path_to_prototypes():
    # Taken from http://stackoverflow.com/a/6098238/732596
    path_to_this_file = dirname(getfile(currentframe()))
    path_to_prototypes = join(path_to_this_file, 'prototypes')
    assert isdir(path_to_prototypes)
    return path_to_prototypes


def all_prototype_filenames():
    # Find all YAML files
    prototype_filenames = []
    def select_prototype_files(prototype_filenames, dirname, fnames):
        new_files = [join(dirname, fname) for fname in fnames 
                     if fname.endswith('.yaml') and fname != 'index.yaml']
        prototype_filenames.extend(new_files)
        fnames = filter(lambda fname: fname != '.git', fnames)

    walk(path_to_prototypes(), select_prototype_files, prototype_filenames)
    return prototype_filenames
    

def filenames_for_prototypes():
    PATH_TO_PROTOTYPES = path_to_prototypes()
    INDEX_FILENAME = join(PATH_TO_PROTOTYPES, 'index.yaml')
    PROTOTYPE_FILENAMES = all_prototype_filenames()

    # check if cache file exists
    if isfile(INDEX_FILENAME):
        # check if any of the prototype files are younger than the index
        mtime_for_index = getmtime(INDEX_FILENAME)
        regenerate_index = False
        for fname in PROTOTYPE_FILENAMES:
            mtime = getmtime(fname)
            if mtime >= mtime_for_index:
                regenerate_index = True
                break
    else:
        regenerate_index = True

    if regenerate_index:
        index_dict = {}
        for fname in PROTOTYPE_FILENAMES:
            prototypes = yaml.load(open(fname))
            if not prototypes:
                continue
            index_dict.update({k:fname for k in prototypes.keys()})

        # Make the filenames relative for caching to disk
        index_dict_relative = {k:v.replace(PATH_TO_PROTOTYPES, '')[1:]
                               for k,v in index_dict.iteritems()}
        with open(INDEX_FILENAME, 'w') as fh:
            yaml.dump(index_dict_relative, fh, default_flow_style=False)
    else:
        with open(INDEX_FILENAME, 'r') as fh:
            index_dict_relative = yaml.load(fh)
        index_dict = {k:join(PATH_TO_PROTOTYPES,v) 
                      for k,v in index_dict_relative.iteritems()}

    return index_dict
