# Bitcoin-easy
A set of utility functions for Bitcoin.  
[![PyPI version](https://badge.fury.io/py/bitcoin-easy.svg)](https://badge.fury.io/py/bitcoin-easy) [![Pull Requests Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## :clipboard: Contents

- [Introduction](#introduction--what-can-you-do-with-bitcoin-easy-)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Examples](#examples)


## Introduction (/ what can you do with bitcoin-easy ?)
You can generate private and derive corresponding public keys, addresses, and in different formats (compressed, uncompressed, WIF).  
You can encrypt your keys in  an universal scheme described in [bip-038](https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki).  
You can also use the functions from [utils.py](https://github.com/darosior/bitcoin-utils/blob/master/utils.py) if you want to do other things (like [base58check](https://github.com/darosior/bitcoin-utils/blob/master/utils.py#L53) encoding, [WIF](https://github.com/darosior/bitcoin-utils/blob/master/utils.py#L46) encoding, pseudo-random generation, [common Bitcoin hashing functions](https://github.com/darosior/bitcoin-utils/blob/master/utils.py#L19)).  
Still in development, more functions to come.

### How ?
```
>>> import bitcoineasy.bitcoineasy as bitcoin
>>> bitcoin.get_keypair()
('L1o65mEUSCgopZUd6hndxqMSvkfvihXV7XmnYoAKt6hWimBXXt6t', '18fyV1xFCXaHXxdjbUnVDBLqFyVnFgrzm1')
>>> bitcoin.encrypt('L1o65mEUSCgopZUd6hndxqMSvkfvihXV7XmnYoAKt6hWimBXXt6t', 'foobar')
'6PYSL5VV8uTFCnCynVdSctyQzm6X2AEJZXG4XQvMu9Bngns2xMeb77JyXH'
```  
   
   
## Installation
You can install bitcoin-easy directly from Pypi using pip :
```
pip install bitcoin-easy
```
To use it from source, you need to install dependencies (see below for more details about dependencies) :
```
git clone https://github.com/darosior/bitcoineasy/ && cd bitcoin-easy
python3 -m venv venv
. venv/bin/activate
pip install py_ecc pycrypto scrypt requests
```
  
  
## Dependencies
- [py_ecc](https://github.com/ethereum/py_ecc) - For the secp256k1 curve
- [pycrypto](https://pypi.org/project/pycrypto/) - For AES
- [scrypt](https://pypi.org/project/scrypt/) - For bip38
- [requests](http://docs.python-requests.org/en/master/) - For entropy
  
  
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
You can also check [example.py](https://github.com/darosior/bitcoineasy/blob/master/bitcoineasy/exemple.py) which is a showcase of some functionalities provided by bitcoin-easy.   

  
### To do
- P2SH
- A better way to handle 0x00 prefix with base58check_decode()
  
  
**_Not finished yet, any remark or feature request are welcome_**
