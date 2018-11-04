# coding: utf8
from .utils import wif_encode, sizeof
from .keys import gen_privkey, get_pubkey, get_address
from .bip38 import encrypt, decrypt

def get_keypair(compressed=True):
    """Generates a new Bitcoin keypair.
    
    Args:
        compressed (bool): if True, the public key will be compressed.
    
    Returns:
        tuple: the private key and the corresponding address, both as str.
    """
    pk = gen_privkey(compressed)
    addr = get_address(get_pubkey(pk))
    return (wif_encode(pk.to_bytes(sizeof(pk), 'big')), addr)


def bip38_encrypt(key, passphrase):
    """Encrypts a private key with a passphrase, as specified in bip38.
    
    Args:  
        key (str|int|bytes): the private key to encrypt.
        passphrase (str): the passphrase that will be needed to decrypt the key.
        
    Returns:
        str: the encrypted private key.
    """
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


def bip38_decrypt(key, passphrase, bin=False):
    """Decrypts a bip38-encrypted Bitcoin private key.
    
    Args:
        key (str|int|byte): key to decrypt.
        passphrase (str): the passphrase used to encrypt the key.
        bin (bool): if True, returns the Bitcoin private key decrypted as bytes.
        
    Returns:
        int : the Bitcoin private key decrypted.
    """
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
