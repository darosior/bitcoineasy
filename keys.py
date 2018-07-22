from py_ecc import secp256k1 # https://github.com/ethereum/py_ecc/blob/master/py_ecc/secp256k1/secp256k1.py
from utils import *

N = 1.158 * pow(10, 77)


def gen_privkey():
    valid = False
    while not valid:
        k = gen_random()
        valid = 0 < k < N
    return k


def get_pubkey_points(privkey):
    (x, y) = secp256k1.privtopub(privkey.to_bytes(sizeof(privkey), 'big'))
    return (x, y)


def get_pubkey(privkey, compressed=True):
    (x, y) = secp256k1.privtopub(privkey.to_bytes(sizeof(privkey), 'big'))
    if not compressed:
        pk = 0x04.to_bytes(1, 'big') + x.to_bytes(sizeof(x), 'big') + y.to_bytes(sizeof(y), 'big')
    else:
        if y%2: # y is odd, so point is greater than the midpoint
            pk = 0x03.to_bytes(1, 'big') + x.to_bytes(sizeof(x), 'big')
        else: # point is less than the midpoint
            pk = 0x02.to_bytes(1, 'big') + x.to_bytes(sizeof(x), 'big')
    return pk


def get_address(pubkey):
    pk_hash = int(hash160(pubkey), 16)
    # Adding the version prefix, then base58check encoding it
    version = 0x00
    address = base58check_encode(pk_hash.to_bytes(sizeof(pk_hash), 'big'), version.to_bytes(1, 'big'))
    return address