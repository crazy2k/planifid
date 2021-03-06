#!/usr/bin/env python
# coding: utf8

"""
Funciones para exportar por XMLRPC
"""

import time

import config
import session
import parsers
import utils
import personal

# cargamos los datos comunes

materias = parsers.parse_materias(config.datadir + '/materias.dat')

carreras = {}
for i in config.carreras.keys():
	f = config.datadir + '/' + config.carreras[i]
	carreras[i] = parsers.parse_carrera(f, materias)


# funciones de la cuenta

def register(username, password):
	"""Registra el usuario y clave, devuelve:
		0 si se registro exitosamente
		1 si el usuario ya existe
		2 si hubo otro problema
	"""
	# TODO: si alguien molesta con esto, hay que armar un mecanismo para
	# evitar DoS (tampoco es muy complicado).

	username = utils.clean(username)
	password = utils.clean(password)
	return personal.register(username, password)


def auth(username, password):
	"""Autentica un usuario, devuelve un string con el session ID, o un
	string vacio si hubo un error de autenticacion."""
	username = utils.clean(username)
	password = utils.clean(password)
	return personal.auth(username, password)


# funciones comunes

def get_carreras():
	"""Devuelve un diccionario { 'COD': 'Descripcion', ... } de las
	carreras disponibles"""
	# FIXME: esto podria hacerse de forma estatica una sola vez, vale la
	# pena?
	d = {}
	for cod in carreras.keys():
		d[cod] = carreras[cod].desc
	return d

def get_areas(carrera):
	"""Devuelve un diccionario { 'COD': 'Descripcion', ... } de las areas
	disponibles en la carrera dada"""
	d = {}
	for area in carreras[carrera].areas.keys():
		d[area] = carreras[carrera].areas[area].desc
	return d

def get_materias(carrera, area):
	"""Devuelve un diccionario { 'COD': 'Descripcion', ... } de las
	materias de la carrera y el area dadas; si el area es un string vacio,
	devuelve todas las materias de la carrera"""
	# FIXME: idem anterior
	if area:
		listam = carreras[carrera].areas[area].materias
	else:
		listam = carreras[carrera].materias.keys()

	d = {}
	for cod in listam:
		# Podriamos usar carreras[carrera].materias[cod]
		# indistintamente, dado que sabemos que la descripcion es
		# igual.
		d[cod] = materias[cod].desc
	return d

def get_correlativas(carrera, materia):
	"""Devuelve un diccionario { 'COD': 'Descripcion', ... } de
	correlativas de una materia"""
	# XXX: se podria optimizar bastante, y con las correlatividades
	# asquerosisimas que tenemos, capaz vendria bien
	l = []
	for i in carreras[carrera].materias[materia].dep:
		if i not in l:
			l.append(i)
	for i in l:
		if ('!' in i) or ('m' in i) or ('c') in i:
			continue
		for j in get_correlativas(carrera, i):
			if j not in l:
				l.append(j)

	d = {}
	for cod in l:
		if '!' in cod:
			d[cod] = materias[cod[1:]].desc
		elif 'm' in cod:
			d[cod] = '%s materias' % cod[:-1]
		elif 'c' in cod:
			d[cod] = '%s créditos' % cod[:-1]
		else:
			d[cod] = materias[cod].desc
	return d

def get_info_materia(carrera, materia):
	mat = carreras[carrera].materias[materia]
	d = dict(
		codigo = materia,
		desc = mat.desc,
		creditos = mat.creditos,
		dep = mat.dep
	)
	return d

# funciones personales

def _sid2per(sid):
	"Devuelve un objeto Personal en base a el session ID"
	username = session.sid_open(sid).username
	return personal.get_personal(username)

def keepalive(sid):
	"Keepalive para la sesion, devuelve el ttl de la misma."
	s = session.sid_open(sid)
	s.touch()
	return s.ttl

def get_personal(sid):
	"Devuelve un diccionario con la informacion personal"
	return _sid2per(sid).todict()

def set_personal(sid, d):
	"""Setea la informacion personal, devuelve 1 si esta todo bien o 0 si
	hubo un error."""
	if not config.carreras.has_key(d['carrera']):
		return 0
	if not carreras[d['carrera']].areas.has_key(d['area']):
		return 0
	if d['hace_tesis'] not in (0, 1):
		return 0
	try:
		# si esto no tira una excepcion, la fecha es valida
		time.strptime("%s/%s/%s" % tuple(d['inicio']), "%d/%m/%Y")
	except:
		print d['inicio']
		return 0
	p = _sid2per(sid)
	p.fromdict(d)
	return 1

def set_passwd(sid, passwd):
	"Setea la clave personal."
	p = _sid2per(sid)
	p.password = passwd
	p.save()
	return 1

def get_estado_materia(sid, materia):
	"""Devuelve el estado de una materia:
		-4	no esta en el plan de estudios
		-3	no se puede cursar por correlatividades
		-2	se puede cursar
		-1	esta cursando
		>= 0	nota
	"""
	p = _sid2per(sid)
	if p.aprobadas.has_key(materia):
		return p.aprobadas[materia]

	if materia in p.cursando:
		return -1

	if not carreras[p.carrera].materias.has_key(materia):
		# no esta en el plan de estudios
		return -4

	# solo nos interesan las correlativas inmediatas
	correlativas = carreras[p.carrera].materias[materia].dep
	for i in correlativas:
		# si no aprobamos alguna correlativa inmediata, fuimos
		if not p.aprobadas.has_key(i):
			return -3

	return -2

def set_estado_materia(sid, materia, estado):
	"""Marca una materia segun el estado:
		-2	no se curso nunca (sirve para corregir errores)
		-1	se esta cursando
		>= 0	nota
	"""
	# TODO: calcular el promedio (que es irreal, no contamos los aplazos,
	# vale la pena?)
	p = _sid2per(sid)
	estado = int(estado)
	if not carreras[p.carrera].materias.has_key(materia):
		return 0
	if estado >= 0:
		p.aprobadas[materia] = estado
		if materia in p.cursando:
			p.cursando.remove(materia)
	elif estado == -1:
		if p.aprobadas.has_key(materia):
			del(p.aprobadas[materia])
		p.cursando.append(materia)
	elif estado == -2:
		if materia in p.cursando:
			p.cursando.remove(materia)
		elif p.aprobadas.has_key(materia):
			del(p.aprobadas[materia])
	else:
		return 0
	p.save()
	return 1

def get_aprobadas(sid):
	"Devuelve un diccionario con las materias aprobadas"
	p = _sid2per(sid)
	d = {}
	for cod in p.aprobadas:
		d[cod] = (p.aprobadas[cod], materias[cod].desc)
	return d

def get_cursando(sid):
	"Devuelve un diccionario con las materias que se estan cursando"
	p = _sid2per(sid)
	d = {}
	for cod in p.cursando:
		d[cod] = materias[cod].desc
	return d

def get_para_cursar(sid):
	"Devuelve un diccionario con las materias que se pueden cursar"
	p = _sid2per(sid)
	l = []
	for cod in carreras[p.carrera].materias.keys():
		if get_estado_materia(sid, cod) == -2:
			l.append(cod)
	d = {}
	for cod in l:
		d[cod] = materias[cod].desc
	return d

# lista de funciones a exportar
list = [
	auth,
	register,
	get_carreras,
	get_areas,
	get_materias,
	get_correlativas,
	get_info_materia,
	keepalive,
	get_personal,
	set_personal,
	set_passwd,
	get_estado_materia,
	set_estado_materia,
	get_aprobadas,
	get_cursando,
	get_para_cursar
]

