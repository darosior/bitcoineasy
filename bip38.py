# coding: utf8

from utils import *
from keys import *
import scrypt
from Crypto.Cypher import AES

# Encryption and decryption of private keys, as described in bip38 : https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
# Ec multiply not available for now

# Takes <key> as str or int and <passphrase> as str. Returns an encrypted private key.
def encrypt(key, passphrase):
    # First get the key format
    if isinstance(key, str): # maybe WIF
        if key[0] == "L" or key[0] == "K": # compressed
            compressed = True
            flag = '\xe0'
            address = get_address(get_pubkey(wif_decode(key, compressed)))
        else if key[0] == "5":
            compressed = False
            flag = '\xc0'
            address = get_address(get_pubkey(wif_decode(key)))
        else:
            raise ValueError("Bad private key format")
    else if isinstance(key, int):
        if key.to_bytes(sizeof(key), 'big')[sizeof(key)-1] == 0x01.to_bytes(1, 'big'):
            compressed = True
            flag = '\xe0'
        else:
            compressed = False
            flag = '\xc0'
        addresshash = get_address(get_pubkey(key.to_bytes(sizeof(key), 'big')))
    else:
        raise ValueError("Private key must be str (WIF encoded) or int")

    addresshash = hashlib.sha256(hashlib.sha256(addr).digest()).digest()[0:4]
    passderived = scrypt.hash(passphrase, addresshash, 16384, 8, 8)
    derivedhalf1 = passderived[0:32]
    derivedhalf2 = passderived[32:64]
    aes = AES.new(derivedhalf2)
