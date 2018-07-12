from hashlib import *

# Returns the ripemd160(sha256(data)), used a lot in Bitcoin
def hash160(data):
	rip = new('ripemd160')
	sha = new('sha256')
	sha.update(str(data).encode())
	rip.update(str(sha.hexdigest()).encode())
	return rip.hexdigest()
	
def base58_encode(data):
	alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	x = data % 58
	rest = data // 58
	if rest == 0:
		return alphabet[x]
	else:
		return base58_encode(rest) + alphabet[x]
		
def base58_decode(data):

# Returns the base58check_encoded data, with prefix "version" 
def base58check_encode(data, version):

def base58check_decode(data):
