
"""
Varias funciones utiles.
"""

import string

def clean(s):
	"Deja en el string s solo las letras, los numeros y '-', '_' y '.'"
	v = ''
	for i in s:
		if i in string.ascii_letters:
			v += i
		if i in '0123456789':
			v += i
		if i in '-_.':
			v += i
	return v

