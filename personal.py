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
		self.aprobadas = {}		# { 'CODIGO': nota, ... }
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


def register(username, password):
	"""Registra el usuario y clave, devuelve:
		0 si se registro exitosamente
		1 si el usuario ya existe
		2 si hubo otro problema
	"""
	username = utils.clean(username)
	password = utils.clean(password)

	# vemos si existe (medio feo, pero por ahora funciona, dependemos de
	# que get_personal tira una excepcion si el usuario no existe)
	p = None
	try:
		p = get_personal(username)
	except:
		pass
	if p != None:
		return 1

	p = Personal()
	p.username = username
	p.password = password

	try:
		p.save()
	except:
		return 2
	return 0


def auth(username, password):
	"""Autentica un usuario, devuelve un string con el session ID, o un
	string vacio si hubo un error de autenticacion."""
	#try:
	p = get_personal(username)
	try:
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


