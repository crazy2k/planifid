#!/usr/bin/env python

"""
Manipulacion de la informacion personal
"""

import os
import pickle

import config
import utils
import session

class Personal:
    "Representa la informacion personal y el estado de una carrera"
    def __init__(self):
        self.username = ''
        self.nombre = ''
        self.padron = ''
        self.password = ''
        self.carrera = ''
        self.aprobadas = {}        # { 'CODIGO': nota, ... }
        self.cursando = []
        self.inicio = []
        self.hace_tesis = 0
        self.area = ''
        self.promedio = 0

    def save(self):
        f = config.personal.basedir + '/' + self.username
        fd = open(f, 'w')
        pickle.dump(self, fd)
        fd.close()

    def todict(self):
        "Convierte la informacion personal en un diccionario"
        d = {}
        d['username'] = self.username
        d['nombre'] = self.nombre
        d['padron'] = self.padron
        d['carrera'] = self.carrera
        d['aprobadas'] = self.aprobadas
        d['cursando'] = self.cursando
        d['inicio'] = self.inicio
        d['hace_tesis'] = self.hace_tesis
        d['area'] = self.area
        d['promedio'] = self.promedio
        return d

    def fromdict(self, d):
        "De un diccionario acomoda la informacion personal"
        self.nombre = d['nombre']
        self.padron = d['padron']
        self.carrera = d['carrera']
        self.area = d['area']
        self.hace_tesis = d['hace_tesis']
        self.inicio = d['inicio']
        self.save()


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
    i = []  # i is the <indication>
    if not utils.passes_filter(username):
        i.append('username')

        if utils.passes_filter(password):
            i.append('password')

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


