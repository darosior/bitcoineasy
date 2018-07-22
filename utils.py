# coding: utf8
from hashlib import *
from math import log

# To get the size in bytes of an integer, https://stackoverflow.com/questions/14329794/get-size-of-integer-in-python
def sizeof(n):
	if n == 0:
		return 1
	return int(log(n, 256)) + 1

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
		
#def base58_decode(data):

# WIF-encode data (as bytes) provided. If the data (which likely be a private key) corresponds to a compressed pk
def wif_encode(data, compressed=False):
	if compressed:
		data = data + 0x01.to_bytes(1, 'big')
	return base58check_encode(data, 0x80.to_bytes(1, 'big'))

# Returns the base58check_encoded data, with prefix "version". <n> and <version> bytes
def base58check_encode(n, version):
	shasha = double_sha256(version+n) #str
	checksum = int(shasha[:8], 16).to_bytes(4, 'big') # First four bytes
	if int.from_bytes(version, 'big') == 0: #else leading zeros are wiped
		return base58_encode(int.from_bytes(version, 'big'))+base58_encode(int.from_bytes(n+checksum, 'big'))
	else:
		return base58_encode(int.from_bytes(version+n+checksum, 'big'))

#def base58check_decode(data):
