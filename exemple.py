# coding: utf8
from main import *

# Generate a basic (nothing compressed) Bitcoin "account" : an address and its corresponding private key
kp = get_keypair()
print("Address : ", kp[1])
print("Private key : ", kp[0])
