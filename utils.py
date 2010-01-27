
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


def iter_data(data, uni = '', fac = ''):
    """Devuelve un iterador sobre el diccionario data filtrado segun
    los valores correspondientes a una universidad y facultad pasados
    por parametro.
    
    El iterador devuelve (uni_code, uni_value, fac_code, fac_value)
    donde los items representan las claves y valores de cada universidad
    y facultad en el diccionario."""

    base = data
    # si se especifica una universidad, iteramos solo sobre sus datos
    if uni:
        base = {uni: data[uni]}

    for uni_code, uni_value in base.iteritems():

        faculties = uni_value['faculties']
        # si se especifica una facultad, iteramos solo sobre sus datos
        if fac:
            faculties = {fac: uni_value['faculties'][fac]}

        for fac_code, fac_value in faculties.iteritems():
            yield (uni_code, uni_value, fac_code, fac_value)


def invalids(named_objs, pred):
    r = []
    for obj, name in named_objs.iteritems():
        if not pred(obj):
            r.append(name)

    return r
