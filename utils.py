# coding: utf8
from hashlib import *
from math import log
from random import randint
from time import time
from math import *
from hashlib import *
from requests import get


# To get the size in bytes of an integer, https://stackoverflow.com/questions/14329794/get-size-of-integer-in-python
from typing import List


def sizeof(n):
	if n == 0:
		return 1
	return int(log(n, 256)) + 1


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


# Returns the ripemd160(sha256(bytes)), used a lot in Bitcoin
def hash160(bytes):
	rip = new('ripemd160')
	rip.update(sha256(bytes).digest())
	return rip.hexdigest() #str


# Returns the sha256(sha256(bytes)), also used a lot
def double_sha256(bytes):
    h = sha256(bytes)
    return sha256(h.digest()).hexdigest() #str


# Takes a number (hex or dec) and returns its base58_encoding
def base58_encode(n):
	alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	x = n % 58
	rest = n // 58
	if rest == 0:
		return alphabet[x]
	else:
		return base58_encode(rest) + alphabet[x]


# Takes a string (base58 encoded number) and returns the base10 number
def base58_decode(string):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    # Populating a dictionary with base58 symbol chart
    dict = {}
    k = 0
    for i in alphabet:
        dict[i] = k
        k+=1
    n = 0 # Result
    pos = 0 # Cf https://www.dcode.fr/conversion-base-n
    for i in string:
        for y in alphabet:
            if i == y:
                n = n * pow(58, pos) + dict[i]
        pos += 1
    return floor(n) # To have an int

# Returns the base58check_encoded data, with prefix "version". <n> and <version> bytes
def base58check_encode(n, version):
	shasha = double_sha256(version+n) #str
	checksum = int(shasha[:8], 16).to_bytes(4, 'big') # First four bytes
	if int.from_bytes(version, 'big') == 0: #else leading zeros are wiped
		return base58_encode(int.from_bytes(version, 'big'))+base58_encode(int.from_bytes(n+checksum, 'big'))
	else:
		return base58_encode(int.from_bytes(version+n+checksum, 'big'))


#def base58check_decode(data):


# WIF-encode data (as bytes) provided. If the data (which likely be a private key) corresponds to a compressed pk
def wif_encode(data, compressed=False):
	if compressed:
		data = data + 0x01.to_bytes(1, 'big')
	return base58check_encode(data, 0x80.to_bytes(1, 'big'))
