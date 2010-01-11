#!/usr/bin/env python

# funciones que recorren el arbol de directorios

import os
import utils
	
def dir_to_dict(path, base_data = None, prev_base_data = None):

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


# parsers, siempre un embole


import string

import config
from clases import Carrera, Area, Materia


def parse_materias(filename):
	"Parsea el archivo con la lista de todas las materias"
	materias = {}

	linenum = 0
	fd = open(filename)

	for line in fd.readlines():
		linenum += 1
		line = line.strip()
		line = line.decode(config.data_encoding).encode('utf-8')

		if not line or line[0] == '#':
			continue
		if '#' in line:
			# ignoramos lo que haya despues del '#'
			i = line.index('#')
			line = line[:i]

		try:
			cod, desc = string.split(line, None, 1)
			desc = desc.strip()
			creditos = int(desc[-2:])
			desc = desc[:-2].strip()
		except:
			raise 'ParseError', (linenum, 'Error parseando linea')

		mat = Materia()
		mat.cod = cod
		mat.desc = desc
		mat.creditos = int(creditos)

		materias[cod] = mat

	return materias


def parse_carrera(filename, materias):
	"""Parsea el archivo con la descripcion de una carrera, devuelve un
	objeto carrera"""

	carr = Carrera()

	seccion = None

	# inicialmente estamos en un area comun
	area_act = 'COMUN'

	# la cual agregamos a la carrera siempre
	carr.areas['COMUN'] = Area()
	carr.areas['COMUN'].cod = 'COMUN'
	carr.areas['COMUN'].desc = 'Comun'

	linenum = 0

	fd = open(filename)

	for line in fd.readlines():
		linenum += 1
		line = line.strip()
		line = line.decode(config.data_encoding).encode('utf-8')

		if not line or line[0] == '#':
			continue
		if '#' in line:
			# ignoramos lo que haya despues del '#'
			i = line.index('#')
			line = line[:i]

		if line[0] == '[' and ']' not in line:
			# hay [ sin ]
			raise 'ParseError', (linenum, "Hay [ sin ]")

		if line[0] == '[':
			# obtenemos lo de adentro de los corchetes
			line = line[1:-1]
			line = line.strip()

			# si no es ninguna de estas dos, entonces es un area,
			# la agregamos
			if line != 'obligatorias' and line != 'optativas':
				unused, cod, desc = string.split(line, None, 2)
				if cod not in carr.areas.keys():
					carr.areas[cod] = Area()
					carr.areas[cod].cod = cod
					carr.areas[cod].desc = desc

				# y cambiamos el area
				area_act = cod

			else:
				# cambiamos la seccion
				seccion = line

		elif '=' in line:
			# es una asignacion, no nos importa en que seccion
			# estemos, simplemente asignamos si es conocida
			attr, val = string.split(line, '=', 1)

			attr = attr.strip()
			val = val.strip()

			if attr == 'carrera':
				carr.desc = val
			elif attr == 'creditos':
				carr.creditos = int(val)
			elif attr == 'creditos_obl':
				carr.creditos_obl = int(val)
			elif attr == 'creditos_obl_area':
				carr.creditos_obl_area = int(val)
			elif attr == 'creditos_tesis':
				carr.creditos_tesis = int(val)
			elif attr == 'creditos_tprof':
				carr.creditos_tprof = int(val)
			elif attr == 'tiene_tesis':
				if val == '1' or val == 'si':
					val = 1
				elif val == '0' or val == 'no':
					val = 0
				carr.tiene_tesis = val
			else:
				raise 'ParseError', \
					(linenum, "Variable desconocida")

		else:
			# estamos en una seccion
			t = string.split(line, None, 1)
			if len(t) == 1:
				# no tiene dependencias
				cod = t[0]
				dep = ''
			else:
				cod = t[0]
				dep = t[1]

			# limpiamos las dependencias, dejando una lista limpia
			t = string.split(dep, ',')
			dep = []
			for i in t:
				i = i.strip()
				if not i:
					continue
				dep.append(i)

			# esta materia ya existe en la lista general, la creo
			# parse_materias(), aca la copiamos y le rellenamos
			# las dependencias, dado que las correlatividades
			# varian segun la carrera; no es una belleza pero se
			# deja mirar
			import copy
			carr.materias[cod] = copy.deepcopy(materias[cod])
			carr.materias[cod].dep = dep

			# y finalmente la agregamos a la carrera
			carr.areas[area_act].materias.append(cod)
			if seccion == 'obligatorias':
				carr.areas[area_act].obligatorias.append(cod)
			elif seccion == 'optativas':
				carr.areas[area_act].optativas.append(cod)
			else:
				raise 'ParseError', \
					(linenum, 'Seccion no valida')

	return carr


# main() de prueba
def main():
	materias = parse_materias('materias.dat')
	estado_act = parse_personal('personal.dat')
	c = parse_carrera(estado_act.carrera_file, materias)
	estado_act.carrera = c
	print c


# si nos llamaron como programa, corremos el main; esto es para permitir que
# alguien importe el programa como un modulo
if __name__ == '__main__':
	main()


