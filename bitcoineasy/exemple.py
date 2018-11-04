# coding: utf8
from .bitcoineasy import get_keypair, bip38_encrypt, bip38_decrypt

# Generates a basic (nothing compressed) Bitcoin "account" : an address and its corresponding private key
def gen_keypair():
    kp = get_keypair()
    print("Address : ", kp[1])
    print("Private key : ", kp[0])


# Generates a random keypair and check if it's funded
def gen_and_check():
	kp = get_keypair()
	res = requests.get("https://blockchain.info/rawaddr/"+str(kp[1]))
	print("This address' balance is ", json.loads(res.text).get("final_balance"))
	print(".. Too bad you cannot retrieve the key")


# Using bip38 encryption with user-input values
def test_bip38_encrypt():
    pk = input("Enter your private key to encrypt : ")
    pas = input("Enter your passphrase : ")
    encrypted = bip38_encrypt(pk, pas)
    print("Here is your encrypted private key : ", encrypted)


def test_bip38_decrypt():
    while True:
        pk = input("Enter your private key to decrypt : ")
        pas = input("Enter the corresponding passphrase : ")
        decrypted = bip38_decrypt(pk, pas)
        if decrypted:
            print("Passphrase matches. Here is the private key : ", wif_encode(decrypted.to_bytes(sizeof(decrypted), 'big')))
            break
        else:
            print("Passphrase doesn't match the encrypted key. Please try again.")
            print("")


def initiation():
    print("- Hi, I'm John !")
    print("- Hi John, here is a keypair : ")
    gen_keypair()
    print("- Oh, thanks !")
    print("- Do you want to encrypt your private key ?")
    a = input("Just press enter to continue. Enter any value to stop. ")
    if not a:
        test_bip38_encrypt()
        print("- Do you want to decrypt your private key ?")
        b = input("Just press enter to continue. Enter any value to stop. ")
        if not b:
            test_bip38_decrypt()
    print("- Bye John !")

initiation()
