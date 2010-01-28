#!/usr/bin/env python

"""
Manipulacion de la informacion personal
"""

import os
import pickle

import config
import utils
import session

class Progdata:
    def __init__(self, id, uni, fac, prog, inid, inim, iniy):
        self.id = id
        self.uni = uni
        self.fac = fac
        self.prog = prog
        self.ini = (inid, inim, iniy)

        self.passed = []
        self.doing = []

        self.average = 0

    def todict(self):
        d = {
            'id': self.id,
            'uni': self.uni,
            'fac': self.fac,
            'prog': self.prog,
            'inid': self.ini[0],
            'inim': self.ini[1],
            'iniy': self.ini[2],
            'passed': self.passed,
            'doing': self.doing,
        }
            
        return d

    def fromdict(self, d):
        self.id = d['id']
        self.uni = d['uni']
        self.fac = d['fac']
        self.prog = d['prog']
        self.ini = (d['inid'], d['inim'], d['iniy'])
        self.passed = d['passed']
        self.doing = d['doing']

        self.recalculate_avg()

    def recalculate_avg(self):
        pass


class Personal:
    "Representa la informacion personal y el estado de una carrera"
    def __init__(self):
        self.username = ''
        self.password = ''
        self.realname = ''

        self.progdatas = []

    def add_progdata(self, id, uni, fac, prog, inid, inim, iniy):
        self.progdatas.append(Progdata(id, uni, fac, prog, inid, inim, iniy))

    def save(self):
        f = config.personal.basedir + '/' + self.username
        fd = open(f, 'w')
        pickle.dump(self, fd)
        fd.close()

    def todict(self):
        "Convierte la informacion personal en un diccionario"
        d = {
            'username': self.username,
            'realname': self.realname,
            'progdatas': [pd.todict() for pd in self.progdatas],
            }
        return d

    def fromdict(self, d):
        "De un diccionario acomoda la informacion personal"

        self.username = d['username']
        self.realname = d['realname']

        for pd_dict in d['progdatas']:
            pd_added = False
            for pd in self.progdatas:
                if pd.uni == pd_dict['uni'] and pd.fac == pd_dict['fac'] and \
                    pd.prog == pd_dict['prog']:

                    pd.fromdict(pd_dict)
                    pd_added = True

            if not pd_added:
                self.progdatas.append(Progdata(pd_dict['id'], pd_dict['uni'],
                    pd_dict['fac'], pd_dict['prog'], pd_dict['inid'],
                    pd_dict['inim'], pd_dict['iniy']))

        self.save()

    def __repr__(self):
        return '<personal: %s' % str(self.todict())


def load(username):
    "Devuelve un objeto Personal correspondiente al username"

    fd = open(config.personal.basedir + '/' + username)
    return pickle.load(fd)


def isregistered(username):
    try:
        p = get_personal(username)
        # if we get here, then username is registered
        return True
    except:
        return False


def register(username, password):
    """Return:
        * (0, <anything>) if registration succeeds,
        * (1, <anything>) if username already exists
        * (2, <indication>) if there's a validation problem;
          <indication> will be a list with 'username' and/or 'password'
          as elements.
        * (3, <reason>) if there's some other problem. <reason> will
          tell what's the problem about.

        <anything> could be any object; empty string is a good
        candidate.

    """

    # data validation
    named_objs = {'username': username, 'password': password}
    i = utils.invalids(named_objs, utils.passes_filter)
    if i:
        return (2, i)

    # we see whether the username is already registered
    if isregistered(username):
        return (1, '')

    p = Personal()
    p.username = username
    p.password = password

    try:
        p.save()
    except:
        return (3, 'Could not save personal information')

    return (0, '')


def auth(username, password):
    """Autentica un usuario, devuelve un string con el session ID, o un
    string vacio si hubo un error de autenticacion."""
    try:
        p = get_personal(username)
        if p.password != password:
            raise
    except:
        return ''

    s = session.sid_create(username)
    return s.sid


# cache de datos personales
# XXX: no hay locks aca porque el server es serializado; si usamos el server
# con multiples threads hay que revisar el locking de todo esto (que es
# bastante trivial).
cache_lru = []
cache = {}

def get_personal(username):
    "Devuelve el objeto con la informacion personal del usuario dado"
    if username in cache.keys():
        # mantenemos LRU
        cache_lru.remove(username)
        cache_lru.append(username)
        return cache[username]

    p = load(username)

    # agregamos al cache
    cache_lru.append(username)
    cache[username] = p
    if len(cache_lru) > config.personal.cache_max:
        del(cache[cache_lru[0]])
        cache_lru.remove(cache_lru[0])

    return p


