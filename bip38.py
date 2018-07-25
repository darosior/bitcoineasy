# coding: utf8

from utils import *
from keys import *
import scrypt
from Crypto.Cipher import AES

# Encryption and decryption of private keys, as described in bip38 : https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
# Ec multiply not available for now

# Takes <key> as str or int and <passphrase> as str. Returns an encrypted private key.
def encrypt(key, passphrase):
    # First get the key format
    if isinstance(key, str): # maybe WIF
        if key[0] == "L" or key[0] == "K": # compressed
            flag = 0xe0.to_bytes(1, 'big') # 11100000
            key = wif_decode(key, compressed=True) # We need to work with bytes
            address = get_address(get_pubkey(key))
        elif key[0] == "5":
            flag = 0xc0.to_bytes(1, 'big') # 11000000
            key = wif_decode(key)
            address = get_address(get_pubkey(key))
        else:
            raise ValueError("Bad private key format")
    elif isinstance(key, int):
        s = sizeof(key)
        key = key.to_bytes(s, 'big') # We need to work with bytes
        if key[s-1] == 0x01.to_bytes(1, 'big'):
            flag = 0xe0.to_bytes(1, 'big')  # 11100000
        else:
            flag = 0xc0.to_bytes(1, 'big')  # 11000000
        address = get_address(get_pubkey(key))
    else:
        raise ValueError("Private key must be str (WIF encoded) or int")

    addresshash = double_sha256(address.encode(), bin=True)[0:4]
    passderived = scrypt.hash(passphrase, addresshash, 16384, 8, 8)
    derivedhalf1 = passderived[0:32]
    derivedhalf2 = passderived[32:64]
    cipher = AES.new(derivedhalf2)
    encryptedhalf1 = cipher.encrypt( (int.from_bytes(key[0:15], 'big') ^ int.from_bytes(derivedhalf1[0:15], 'big')).to_bytes(16, 'big') )
    encryptedhalf2 = cipher.encrypt( (int.from_bytes(key[16:32], 'big') ^ int.from_bytes(derivedhalf1[16:32], 'big')).to_bytes(16, 'big') )
    return base58check_encode(flag + addresshash + encryptedhalf1 + encryptedhalf2, 0x0142.to_bytes(2, 'big'))

print(encrypt(0xCBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5, 'TestingOneTwoThree'))
print(encrypt('5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR', 'TestingOneTwoThree'))
