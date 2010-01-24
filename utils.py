
"""
Varias funciones utiles.
"""

import string
import os

permitidos = string.ascii_letters + string.digits + '-_.'

def clean(s):
    "Deja en el string s solo los caracteres permitidos"
    v = ''
    count = 0
    for i in s:
        if count == 20:
            break
        if i in permitidos:
            v += i
            count += 1
    return v


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
