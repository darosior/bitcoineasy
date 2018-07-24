# coding: utf8

from utils import *
from keys import *
import scrypt

# Encryption and decryption of private keys, as described in bip38 : https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
# Ec multiply not available for now

def encrypt(key, passphrase):
    # First get the key format
    if isinstance(key, str): # maybe WIF
        if key[0] == "L" or key[0] == "K": # compressed
            compressed = True
            flag = '\xe0'
        else if key[0] == "5":
            compressed = False
            flag = '\xc0'
        else:
            raise ValueError("Bad private key format")
    else if isinstance(key, int):
        if key.to_bytes(sizeof(key), 'big')[sizeof(key)-1] == 0x01.to_bytes(1, 'big'):
            compressed = True
            flag = '\xe0'
        else:
            compressed = False
            flag = '\xc0'
        addresshash = get_address(get_pubkey(key))
    else:
        raise ValueError("Private key must be str (WIF encoded) or int")

    address = get_address(get_pubkey(key))
    addresshash = hashlib.sha256(hashlib.sha256(addr).digest()).digest()[0:4]
