
"""
Archivo de configuracion del planifid
"""

# directorio base para los datos, y donde se almacena la informacion de las
# carreras y las materias
datadir = "./data"

# address y port donde esperar conexiones; si el address es el string vacio,
# espera en todas las ips
addr = ''
port = 8026

# encoding en el cual estan almacenados los archivos de datos (en el tarball
# oficial estan en latin1)
data_encoding = 'latin1'


class session:
	"Configuracion del manejo de sesiones"

	# tiempo de vida estandar de las sesiones, en segundos
	ttl = 10 * 60


class personal:
	"Configuracion de la informacion personal"

	# directorio base de la informacion de los usuarios
	basedir = datadir + '/users'

	# numero maximo de entradas en el cache
	cache_max = 20


# lista de carreras y su respectivo archivo
carreras = {
	'AGR': 'agrimensura.dat',
	'ALI': 'alimentos.dat',
	'CIV': 'civil.dat',
	'ELC': 'electricista.dat',
	'ELE': 'electronica.dat',
	'IND': 'industrial.dat',
	'INF': 'informatica.dat',
	'MEC': 'mecanica.dat',
	'NAV': 'naval.dat',
	'QUI': 'quimica.dat',
	'SIS': 'sistemas.dat',
}


