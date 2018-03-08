import base64
from Crypto.Cipher import DES3
import hashlib
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_key():
    """this is the getKey function that generates an encryption Key for you
        by passing your Secret Key as a parameter.
         """
    secret_key = os.environ.get('SECRET_KEY')
    hashed_secret_key = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
    hashed_secret_key_last_12 = hashed_secret_key[-12:]
    secret_key_adjusted = secret_key.replace('FLWSECK-', '')
    secret_key_adjusted_first12 = secret_key_adjusted[:12]
    print(secret_key_adjusted_first12 + hashed_secret_key_last_12)


"""This is the encryption function that encrypts your payload by passing the text and your encryption Key."""


def encrypt_data(key, plainText):
    blockSize = 8
    padDiff = blockSize - (len(plainText) % blockSize)
    cipher = DES3.new(key, DES3.MODE_ECB)
    plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
    encrypted = base64.b64encode(cipher.encrypt(plainText))
    return encrypted


get_key()
