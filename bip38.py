# coding: utf8

from utils import *
from keys import *
import scrypt
from Crypto.Cipher import AES

# Encryption and decryption of private keys, as described in bip38 : https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
# Ec multiply not available for now

# Takes <key> as str or int and <passphrase> as str. Returns an encrypted private key.
def encrypt(key, passphrase):
    # First handle the key format and pass to bytes
    if isinstance(key, str):
        if key[0] == "5":
            key = wif_decode(key)
        elif key[0] == "L" or key[0] == "K":
            key = wif_decode(key)
        else:
            raise ValueError("Private key passed as first argument is not a valid WIF-encoded privkey")
    elif isinstance(key, int):
        key = key.to_bytes(sizeof(key), 'big')
    # Then we set the flag depending of whether the key is compressed or not
    if key[len(key)-1] == 0x01: # Is compressed
        flag = 0xe0.to_bytes(1, 'big')  # 11100000
    else: # Not compressed
        flag = 0xc0.to_bytes(1, 'big')  # 11000000
    # Then we take the address which will be used as an entropy source
    address = get_address(get_pubkey(key))
    addresshash = double_sha256(address.encode(), bin=True)[:4]
    # We derive a key from the passphrase
    passderived = scrypt.hash(passphrase.encode(), addresshash, 16384, 8, 8)
    # Which we split in 2 parts
    derivedhalf1 = passderived[0:32]
    derivedhalf2 = passderived[32:64]
    # We then encrypt with AES as specified in BIP
    cipher = AES.new(derivedhalf2)
    int1 = int.from_bytes(key[0:16], 'big') ^ int.from_bytes(derivedhalf1[0:16], 'big')
    int2 = int.from_bytes(key[16:32], 'big') ^ int.from_bytes(derivedhalf1[16:32], 'big')
    encryptedhalf1 = cipher.encrypt( int1.to_bytes(sizeof(int1), 'big') )
    encryptedhalf2 = cipher.encrypt( int2.to_bytes(sizeof(int2), 'big') )
    return base58check_encode(flag + addresshash + encryptedhalf1 + encryptedhalf2, 0x0142.to_bytes(2, 'big'))

def test():
    print("No compression : ")
    print("hex : ", encrypt(0xCBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5, 'TestingOneTwoThree'))
    print("wif : ", encrypt('5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR', 'TestingOneTwoThree'))
    print("expected : 6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg")
    print("")
    print("hex : ", encrypt(0x09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE, 'Satoshi'))
    print("wif : ", encrypt('5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5', 'Satoshi'))
    print("expected : 6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq")
    print("")
    print("")
    print("With compression : ")
    print("hex : ", encrypt(0xCBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5, 'TestingOneTwoThree'))
    print("wif : ", encrypt('L44B5gGEpqEDRS9vVPz7QT35jcBG2r3CZwSwQ4fCewXAhAhqGVpP', 'TestingOneTwoThree'))
    print("expected : 6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo")
    print("")
    print("hex : ", encrypt(0x09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE, 'Satoshi'))
    print("wif : ", encrypt('KwYgW8gcxj1JWJXhPSu4Fqwzfhp5Yfi42mdYmMa4XqK7NJxXUSK7', 'Satoshi'))
    print("expected : 6PYLtMnXvfG3oJde97zRyLYFZCYizPU5T3LwgdYJz1fRhh16bU7u6PPmY7")

#test()
