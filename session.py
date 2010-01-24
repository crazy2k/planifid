
"""
Manejo de sesiones
"""

import time
import sha

import config
import utils


class session:
    "Clase que representa los datos de una sesion"
    def __init__(self):
        self.version = 1        # version del formato
        self.username = ''        # username
        self.ctime = time.time()    # fecha de creacion
        self.ttl = config.session.ttl    # ttl en segundos
        self.atime = 0            # ultimo tiempo de acceso
        self.sid = ''            # session id

    def touch(self):
        "Actualiza el tiempo de acceso"
        self.atime = time.time()


# Diccionario de sesiones activas actualmente, indexado por session ID
activas = {}

# TODO: expirar las sesiones y hacer locks
def check_sessions():
    "Revisa las sesiones activas y remueve las expiradas"
    for sid in activas.keys():
        sd = activas[sid]
        print time.time(), sd.atime, time.time() - sd.atime, sd.ttl
        if (time.time() - sd.atime) > sd.ttl:
            del(activas[sid])

def build_sid(sd):
    """Devuelve un string identificador de sesion (sid) que es el shasum
    del username, la version y el tiempo de creacion"""
    #FIXME: agregar un random
    c = sd.username + str(sd.ctime)
    return sha.new(c).hexdigest()



def sid_create(username):
    "Inicia una sesion con un usuario; devuelve una clase de sesion"
    sd = session()
    sd.username = username
    sd.sid = build_sid(sd)
    activas[sd.sid] = sd
    return sd


def sid_open(sid):
    "Devuelve un objeto session correspondiente al sid dado"
    try:
        sd = activas[sid]
        sd.touch()
        return sd
    except:
        raise "UnknownSID"

def sid_remove(sid):
    del(activas[sid])

def validate(sid):
    """Valida si el session id es valido, en base a su tiempo de vida; de
    ser valida devuelve el sd"""
    try:
        sd = sid_open(sid)
        if (time.time() - sd.atime ) > sd.ttl:
            return 0
    except:
        return 0
    sd.touch()
    return sd



