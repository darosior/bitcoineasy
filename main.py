# coding: utf8
from random import randint
from math import *
from hashlib import *
from requests import get
from time import time
from utils import *
from py_ecc import secp256k1 # https://github.com/ethereum/py_ecc/blob/master/py_ecc/secp256k1/secp256k1.py

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

def gen_privkey():
	valid = False
	while not valid:
		k = gen_random()
		valid = 0 < k < N
	return k
	
def get_pubkey_points(privkey):
	(x, y) = secp256k1.privtopub(privkey.to_bytes(32, 'big'))
	return (x, y)

def get_pubkey(privkey):
	(x, y) = secp256k1.privtopub(privkey.to_bytes(32, 'big'))
	pk = 0x04.to_bytes(1, 'big') + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')
	return pk #bytes

def get_address(pubkey):
	pk_hash = int(hash160(pubkey), 16)
	# Adding the version prefix, then base58check encoding it
	address = base58check_encode(pk_hash, 0x00)
	return address
	
print(get_address(get_pubkey(0x18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725)))

