# coding: utf8

from utils import sizeof, double_sha256, base58check_encode, base58check_decode, wif_decode
from keys import get_address, get_pubkey
import scrypt
from Crypto.Cipher import AES

"""
Encryption and decryption of private keys, as described in bip38 : https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
Ec multiply not available for now
"""

def encrypt(key, passphrase):
    """Encrypts a Bitcoin private key as described in bip38.
    
    Args:
        key (int|str): a Bitcoin private key.
        passphrase (str): the passphrase that will decrypt the private key.
        
    Returns:
        str: the encrypted private key.
    """
    # First handle the key format and pass to bytes
    if isinstance(key, str):
        if key[0] == "5":
            key = wif_decode(key)
        elif key[0] == "L" or key[0] == "K":
            key = wif_decode(key) # Not specifying compressed here, cause it would wipe the last 0x01 byte
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


def decrypt(key, passphrase):
    """Decrypts an encrypted Bitcoin private key.
    
    Args:
        key (str): an encrypted Bitcoin private key.
        passphrase (str): the passphrase used to encrypt the private key.
        
    Returns:
        bytes: the private key.
    """
    # Doing the reverse scheme
    dec = base58check_decode(key, n=2) # Version is 2 bytes length, cf encrypt()
    flag = dec[:1]
    addresshash = dec[1:5]
    encryptedhalf1 = dec[5:21]
    encryptedhalf2 = dec[21:37]
    passderived = scrypt.hash(passphrase.encode(), addresshash, 16384, 8, 8)
    derivedhalf1 = passderived[0:32]
    derivedhalf2 = passderived[32:64]
    cipher = AES.new(derivedhalf2)
    decryptedhalf1 = cipher.decrypt(encryptedhalf1)
    decryptedhalf2 = cipher.decrypt(encryptedhalf2)
    # Inverse of XOR is ... XOR
    privkey = int.from_bytes(decryptedhalf1+decryptedhalf2, 'big') ^ int.from_bytes(derivedhalf1, 'big')
    privkey = privkey.to_bytes(sizeof(privkey), 'big')
    if flag == 0xe0.to_bytes(1, 'big'): # Compressed
        privkey = privkey + 0x01.to_bytes(1, 'big')
        address = get_address(get_pubkey(privkey))
    elif flag == 0xc0.to_bytes(1, 'big'): # Not compressed
        address = get_address(get_pubkey(privkey))
    else:
        raise ValueError("Key passed as first parameter was malformed. Couldn't read flag byte.")
    if double_sha256(address.encode(), bin=True)[:4] == addresshash:
        return privkey # type : bytes
    else:
        return False


def test():
    """Run the tests with values given in bip.
    CAUTION : I added a 0 to compressed keys in order to have them in hex-compressed format.
    """
    print("Test with no compression : ")
    print(" Test 1")
    hex = encrypt(0xCBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5, 'TestingOneTwoThree')
    wif = encrypt('5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR', 'TestingOneTwoThree')
    expected = '6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg'
    decrypted = decrypt(expected, 'TestingOneTwoThree')
    if hex == expected and wif == expected:
        print("     Encryption OK")
    else:
        print("     Encryption failed")
        print("     hex : ", hex)
        print("     wif : ", wif)
        print("     expected : ", expected)
    if decrypted and int.from_bytes(decrypted, 'big') == 0xCBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5:
        print("     Decryption OK")
    else:
        print("     Decryption Failed")
        print("     decrypted : ", decrypted)

    print("")

    print(" Test 2")
    hex = encrypt(0x09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE, 'Satoshi')
    wif = encrypt('5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5', 'Satoshi')
    expected = '6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq'
    decrypted = decrypt(expected, 'Satoshi')
    if hex == expected and wif == expected:
        print("     Encryption OK")
    else:
        print("     Encryption failed")
        print("     hex : ", hex)
        print("     wif : ", wif)
        print("     expected : ", expected)
    if decrypted and int.from_bytes(decrypted, 'big') == 0x09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE:
        print("     Decryption OK")
    else:
        print("     Decryption Failed")
        print("     decrypted : ", decrypted)

    print("")

    print("")
    print("Test with compression : ")
    print(" Test 1")
    # Here I don't know why there is no 0x01 for compressed privkey so I added it
    hex = encrypt(0xCBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A501, 'TestingOneTwoThree')
    wif = encrypt('L44B5gGEpqEDRS9vVPz7QT35jcBG2r3CZwSwQ4fCewXAhAhqGVpP', 'TestingOneTwoThree')
    expected = '6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo'
    decrypted = decrypt(expected, 'TestingOneTwoThree')
    if hex == expected and wif == expected:
        print("     Encryption OK")
    else:
        print("     Encryption failed")
        print("     hex : ", hex)
        print("     wif : ", wif)
        print("     expected : ", expected)
    if decrypted and int.from_bytes(decrypted, 'big') == 0xCBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A501:
        print("     Decryption OK")
    else:
        print("     Decryption Failed")
        print("     decrypted : ", decrypted)

    print("")

    print(" Test 2")
    # Here I don't know why there is no 0x01 for compressed privkey so I added it
    hex = encrypt(0x09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE01, 'Satoshi')
    wif = encrypt('KwYgW8gcxj1JWJXhPSu4Fqwzfhp5Yfi42mdYmMa4XqK7NJxXUSK7', 'Satoshi')
    expected = '6PYLtMnXvfG3oJde97zRyLYFZCYizPU5T3LwgdYJz1fRhh16bU7u6PPmY7'
    decrypted = decrypt(expected, 'Satoshi')
    if hex == expected and wif == expected:
        print("     Encryption OK")
    else:
        print("     Encryption failed")
        print("     hex : ", hex)
        print("     wif : ", wif)
        print("     expected : ", expected)
    if decrypted and int.from_bytes(decrypted, 'big') == 0x09C2686880095B1A4C249EE3AC4EEA8A014F11E6F986D0B5025AC1F39AFBD9AE01:
        print("     Decryption OK")
    else:
        print("     Decryption Failed")
        print("     decrypted : ", decrypted)


if __name__ == '__main__':
    test()
