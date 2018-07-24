# Bitcoin-utils
A set of utility functions for Bitcoin.

## What can you do with it ?
For now, I'm doing the key part.  
You can generate private and derive corresponding public keys, addresses, and in different formats (compressed, uncompressed, WIF).  
You can also use the functions from [utils.py](https://github.com/darosior/bitcoin-utils/blob/master/utils.py) if you want to do other things (like [base58check](https://github.com/darosior/bitcoin-utils/blob/master/utils.py#L53) encoding, [WIF](https://github.com/darosior/bitcoin-utils/blob/master/utils.py#L46) encoding, pseudo-random generation, [common Bitcoin hashing functions](https://github.com/darosior/bitcoin-utils/blob/master/utils.py#L19)).  

## How ?
Just clone the repo and import main.py for now.  
   
## Dependencies
scrypt
```
pip3 install scrypt
```
py_ecc (https://github.com/ethereum/py_ecc) for secp256k1

## Examples
Generate a keypair (default is compressed public key and WIF encoded private key) : 
```
kp = get_keypair()
```
If you want unencoded private key (diplayed as hex) and uncompressed public key : 
```
kp = get_keypair(compressed=False, wif=False)
```
You can base58 or base58check encode raw bytes with : 
```
base58_encode(data)
base58check_encode(data)
```
   
   
See the example.py file for more.
  
### To do
- P2SH
- bip38
- A better way to handle 0x00 prefix with base58check_decode()
  
### Sources
https://en.bitcoin.it/wiki/Base58Check_encoding  
https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki  
https://github.com/bitcoin/  
https://masteringbitcoin.neocities.org/  
https://bitcoin.org/  
https://bitcointalk.org/  
  
**_Not finished yet, any remark or feature request are welcome_**
