# coding: utf8
from keys import *
from bip38 import *

# Returns a tuple of an address and its corresponding private key
def get_keypair(compressed=True):
    pk = gen_privkey(compressed)
    addr = get_address(get_pubkey(pk))
    return (wif_encode(pk.to_bytes(sizeof(pk), 'big')), addr)


# Returns a private key encrypted with the passphrase as str. key can be str, int or bytes. passphrase must be str.
def bip38_encrypt(key, passphrase):
    if not isinstance(key, int) and not isinstance(key, str) and not isinstance(key, bytes):
        raise ValueError("<key> must be int bytes or str")
    if isinstance(key, str): # If a hex-key is passed as str
        try:
            if key[0] not in ["K", "L", "5"]:
                key = int(key, 16)
        except:
            raise ValueError(" if <key> is str it must be WIF encoded or an hex number")
    if not isinstance(passphrase, str):
        raise ValueError("<passphrase> must be str")
    return encrypt(key, passphrase) # type : str


# Returns a private key if succeeds to decrypt, False otherwise.
# key can be str, int or bytes. passphrase must be str.
# If bin is set to true, the raw key will be returned.
def bip38_decrypt(key, passphrase, bin=False):
    if not isinstance(key, int) and not isinstance(key, str) and not isinstance(key, bytes):
        raise ValueError("<key> must be int bytes or str")
    if isinstance(key, int): # If a hex-key is passed as str
        key = str(key)
    elif isinstance(key, bytes):
        key = str(int.from_bytes(key, 'big'))
    if not isinstance(passphrase, str):
        raise ValueError("<passphrase> must be str")
    decrypted = decrypt(key, passphrase)
    if bin:
        return decrypted # type : bytes
    else:
        if decrypted: # Can be False
            return int.from_bytes(decrypted, 'big') # type: int
