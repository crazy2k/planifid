#!/usr/bin/env python

# clases para representar la informacion del planifi


class Carrera:
	"""Representa una carrera, con algunos atributos y una lista de
	materias que la componen"""

	def __init__(self):
		self.desc = ''
		self.creditos = ''
		self.creditos_obl = ''
		self.creditos_obl_area = ''
		self.creditos_tesis = ''
		self.creditos_tprof = ''

		# una carrera tiene siempre un area denominada 'comun', y
		# puede opcionalmente tener otras segun especialidades.
		self.areas = {}

		# las materias se guardan en un diccionario indexado por el
		# codigo de la materia, y como valor el objeto de la materia
		# que representa, dado que segun la carrera, las dependencias
		# de las materias varien.
		self.materias = {}

	def __repr__(self):
		return '<carrera: desc="%s">' % str(self.desc)


class Materia:
	"""Representa una materia, compuesta de un codigo, una descripcion, los
	creditos y una lista de codigos de dependencia"""

	def __init__(self):
		self.cod = ''
		self.desc = ''
		self.creditos = 0
		self.dep = []

	def __repr__(self):
		return '<materia: cod=%s desc="%s">' % (self.cod, self.desc)

	def correlativas(self):
		"Devuelve la lista de correlativas"
		c = []
		for codigo in self.dep:
			c.append(materias[codigo])
		return c


class Area:
	"Area de una carrera"
	def __init__(self):
		self.cod = ''
		self.desc = ''
		self.materias = []
		self.obligatorias = []
		self.optativas = []


class Estado:
	"""Representa el estado de una carrera, o sea, las materias aprobadas,
	notas, promedios, etc."""

	def __init__(self):
		self.carrera = ''
		self.carrera_file = ''
		self.aprobadas = {}		# { 'CODIGO': nota, ... }
		self.cursando = []
		self.inicio = []
		self.hace_tesis = 0
		self.area = ''
		self.promedio = 0


	def __repr__(self):
		return '<estado: carrera=%s area=%s>' % (self.carrera, self.area)



