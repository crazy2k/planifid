
"""
Various utilities.
"""

import os
import string
import re
import time


#
# Data validation stuff
#


class Validator:
    def __call__(self, s):
        return self.pred(s)


class ValidatorRE(Validator):
    def __init__(self, regexp, err):
        compiled_re = re.compile(regexp)
        self.pred = lambda s: bool(compiled_re.match(s))
        self.err = err


class ValidatorPred(Validator):
    def __init__(self, pred, err):
        self.pred = pred
        self.err = err


def _date_is_valid(date):
    try:
        # if this doesn't raise an exception, date is valid
        time.strptime(date, "%d/%m/%Y")
        return True
    except ValueError:
        return False

username_err = 'Username may contain common letters, numbers and the \
    characters "_", "." and "-", and its length must be less than 20.'
password_err = 'Password may contain common letters, numbers and the \
    characters "_", "." and "-", and its length must be less than 20.'
realname_err = 'Real names may contain common letters, numbers and the \
    characters "_", "." and "-", and its length must be less than 40.'

# dictionary with validator functions for each field
validators = {
    'username': ValidatorRE(r'^[a-z0-9-_.]{1,20}$', username_err),
    'password': ValidatorRE(r'^[a-z0-9-_.]{1,20}$', password_err),
    'realname': ValidatorRE(r'^[a-z0-9-_.]{0,40}$', realname_err),
    'date': ValidatorPred(_date_is_valid, 'Date must be a valid date.'),
}


#
# Other functions
#

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


def invalids(named_objs, pred = None, err_msg = True):
    r = []
    for name, obj in named_objs.iteritems():
        # if a predicate is given, we use it for every obj
        if pred:
            pred.err = ''
            valid = pred
        # if not, use corresponding validators
        else:
            valid = validators[name]

        if not valid(obj):
            if err_msg:
                r.append((name, valid.err))
            else:
                r.append(name)
                
    return r
