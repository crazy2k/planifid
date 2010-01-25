
"""
Varias funciones utiles.
"""

import string
import os

nice_chars = string.ascii_letters + string.digits + '-_.'

def filterstr(s, allowed = nice_chars):
    new = [c for c in s if c in allowed]
    new = string.join(new, '')
    return new

def passes_filter(s, allowed = nice_chars):
    return s == filterstr(s, allowed)

def get_file_contents(fpath):
    fd = open(fpath)
    contents = fd.read()
    fd.close()

    return contents

def add_path(path, fnames):
    return [(os.path.join(path, fname), fname) for fname in fnames]

def gen_key(*parts):
    r = parts[0]
    for p in parts[1:]:
        r += '/' + p
    
    return r
