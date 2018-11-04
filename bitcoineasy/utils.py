# coding: utf8
from hashlib import sha256, new
from random import randint
from time import time
from math import log, floor
import requests as r


def sizeof(n):
	"""get the size in bytes of an integer, https://stackoverflow.com/questions/14329794/get-size-of-integer-in-python
	
	Args:
            n (int): the integer to get the size
	    
	Returns:
	    int: the size in bytes of the first parameter.
	"""
	if n == 0:
		return 1
	return int(log(n, 256)) + 1


def gen_random():
	"""Generates a pseudo-random integer.

	Returns:
	    int: a pseudo-random number.
	"""
	h = sha256()
	# 2 or 3 differents sources of entropy
	h.update(str(randint(0, pow(2, 256))).encode())
	h.update(str(time()).encode())
	try:
		req = r.get("https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard")
		h.update(str(req.content).encode())
	except:
		pass
	finally:
		return int(h.hexdigest(), 16)


def hash160(bytes, bin=False):
    """Returns the ripemd160(sha256(data)), used a lot in Bitcoin.
    
    Args:
        bytes (bytes): the data to hash.
	bin (bool): if set to True, returns bytes.
    
    Returns:
        str/bytes: the hash of the data passed as first parameter.
    """
    rip = new('ripemd160')
    rip.update(sha256(bytes).digest())
    if bin:
        return rip.digest()  # type : bytes
    else:
    	return rip.hexdigest() # type : str


def double_sha256(bytes, bin=False):
    """Returns the sha256(sha256(data)), used a lot in Bitcoin.
    
    Args:
        bytes (bytes): the data to hash.
	bin (bool): if set to True, returns raw data

    Returns:
        str/bytes: the hash of the data passed as first parameter.
    """
    h = sha256(bytes)
    if bin:
        return sha256(h.digest()).digest() # type : bytes
    else:
        return sha256(h.digest()).hexdigest() # type : str


def base58_encode(n):
    """Takes a number (hex or dec) and returns its base58_encoding.
    
    Args:
    	n (int): the number to base58_encode.
	
    Returns:
    	str: the number passed as first parameter, base58 encoded.
    """
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    x = n % 58
    rest = n // 58
    if rest == 0:
        return alphabet[x]
    else:
        return base58_encode(rest) + alphabet[x]


def base58_decode(string):
    """Takes a base58-encoded number and returns it in base10.
    
    Args:
    	string (str): the number to base58_decode.
	
    Returns:
    	int: the number passed as first parameter, base10 encoded.
    """
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
                n = n * 58 + dict[i]
        pos += 1
    return n


def base58check_encode(n, version):
    """Returns the base58check_encoded data, with prefix "version".
	
	Args:
	    n (bytes): the data to base58check encode.
	    version (bytes): the prefix to set during encoding.
	
	Returns:
	    str: the data encoded in base58check.
	"""
    shasha = double_sha256(version+n) #str
    checksum = int(shasha[:8], 16).to_bytes(4, 'big') # First four bytes
    if int.from_bytes(version, 'big') == 0: # Else leading zeros are wiped
        return base58_encode(int.from_bytes(version, 'big'))+base58_encode(int.from_bytes(n+checksum, 'big'))
    else:
        return base58_encode(int.from_bytes(version+n+checksum, 'big'))


def base58check_decode(string, n=1, zero=False):
    """Returns the base58check_decoded data. Please notice the "zero" parameter.
	
    Args:
        string (str): the data to decode.
	n (int): the prefix's size (in bytes). 1 in most cases.
        zero (bool): to set to True if the string specified was encoded with a 0x00 prefix.
	
    Returns:
        str: the data encoded in base58check.
    """
    data = base58_decode(string)
    if zero:
        return data.to_bytes(sizeof(data), 'big')[:sizeof(data)-4]
    else:
        return data.to_bytes(sizeof(data), 'big')[n:sizeof(data) - 4]


def wif_encode(data):
	"""WIF-encode data (which would likely be a Bitcoin private key) provided.
	
	Args:
	    data (bytes): the data to encode.
	    
	Returns:
	    str: the WIF-encoded data.
	"""
	return base58check_encode(data, 0x80.to_bytes(1, 'big'))


def wif_decode(string):
    """WIF-decode string (which would likely be a WIF-encoded Bitcoin private key) provided.
	
    Args:
        string (str): the data to decode.
	    
    Returns:
        str: the WIF-encoded data.
    """
    dec = base58check_decode(string)
    compressed = string[0] == 'K' or string[0] == 'L'
    if compressed:
        return dec[:len(dec)-1]
    else:
        return dec
