# coding: utf8
from main import *
import requests
import json

# Generate a basic (nothing compressed) Bitcoin "account" : an address and its corresponding private key
kp = get_keypair()
print("Address : ", kp[1])
print("Private key : ", kp[0])

# Generates a random keypair and check if it's funded
def gen_and_check():
	kp = get_keypair()
	res = requests.get("https://blockchain.info/rawaddr/"+str(kp[1]))
	print("This address' balance is ", json.loads(res.text).get("final_balance"))
	print(".. Too bad you cannot retrieve the key")
	
#gen_and_check()
	
