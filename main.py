# coding: utf8
from utils import *



# Returns a tuple of an address and its corresponding private key
def get_keypair(compressed=False):
    pk = gen_privkey()
	if not compressed:
		addr = get_address(get_pubkey(pk))
	    return (wif_encode(pk.to_bytes(sizeof(pk), 'big')), addr)