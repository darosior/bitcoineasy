# coding: utf8
from keys import *

# Returns a tuple of an address and its corresponding private key
def get_keypair(compressed=True):
	pk = gen_privkey(compressed)
	addr = get_address(get_pubkey(pk))
	return (wif_encode(pk.to_bytes(sizeof(pk), 'big')), addr)
