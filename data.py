"""
Data gathering module
"""

import os

import config
import parsers
import utils
    

def dirpath_to_dict(path, base_data = None, prev_base_data = None):
    """From a path to a directory, walk it and construct a dictionary
    whose structure mimics the one of the tree and has domain-specific
    objects instead of data files, and then return it.

    """

    data = {}

    if base_data is not None:
        data = base_data

    # observamos un solo nivel
    _, dnames, fnames = os.walk(path).next()

    # primero los archivos
    for fpath, fname in utils.add_path(path, fnames):
        if fname in ['name']:
            data[fname] = utils.get_file_contents(fpath)
        elif fname == 'courses':
            data[fname] = parse_materias(fpath)
        elif os.path.basename(path) == 'programs':
            data[fname] = parse_carrera(fpath,
                prev_base_data['courses'])
    
    # despues los directorios
    for dpath, dname in utils.add_path(path, dnames):
        data[dname] = {}

        dir_to_dict(dpath, data[dname], data)

    return data

datadict = dirpath_to_dict(config.unisdir)


