
"""
Varias funciones utiles.
"""

import string

permitidos = string.ascii_letters + string.digits + '-_.'

def clean(s):
	"Deja en el string s solo los caracteres permitidos"
	v = ''
	count = 0
	for i in s:
		if count == 20:
			break
		if i in permitidos:
			v += i
			count++
	return v

