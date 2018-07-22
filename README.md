# Bitcoin-utils
A set of utility functions for Bitcoin.

## What can you do with it ?
For now, I'm doing the key part.  
You can generate private and public keys, adresses, and in different formats (compressed, uncompressed, WIF).  
You can also use the functions from utils.py if you want to do other things (like base58check encoding, WIF encoding, pseudo-random generation, popular Bitcoin hashing functions).  

## How ?
Just clone the repo and import main.py for now.  

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
  
**_Not finished yet, any remark or feature request are welcome_**
