from random import randint
from math import *
from hashlib import *
from requests import get
from time import time

N = 1.158 * pow(10, 77)

def gen_random():
	h = sha256()
	# 2 or 3 differents sources of entropy 
	h.update(str(randint(0, pow(2, 256))).encode())
	h.update(str(time()).encode())
	try:
		req = get("https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard")
		h.update(str(req.content).encode())
	except:
		pass
	finally:
		return int(h.hexdigest(), 16)

	
