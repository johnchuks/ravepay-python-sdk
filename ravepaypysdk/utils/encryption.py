import base64
import json
from Crypto.Cipher import DES3
import hashlib


def get_key(secret_key):
    """this is the getKey function that generates an encryption Key for you
        by passing your Secret Key as a parameter.
         """
    hashed_secret_key = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
    hashed_secret_key_last_12 = hashed_secret_key[-12:]
    secret_key_adjusted = secret_key.replace('FLWSECK-', '')
    secret_key_adjusted_first12 = secret_key_adjusted[:12]
    return secret_key_adjusted_first12 + hashed_secret_key_last_12


def encrypt_data(secret_key, plain_text):
    """
    This is the encryption function that encrypts your
     payload by passing the text and your encryption Key.
    """
    encrypted_key = get_key(secret_key)
    block_size = 8
    toAdd = len(plain_text) % block_size
    pad_diff = block_size - toAdd
    cipher = DES3.new(encrypted_key, DES3.MODE_ECB)
    plain_text = "{}{}".format(plain_text, "".join(chr(pad_diff) * pad_diff))
    encrypted = base64.b64encode(cipher.encrypt(plain_text))
    decrypting = base64.b64decode(encrypted)
    decrypted = cipher.decrypt(decrypting)
    return encrypted


