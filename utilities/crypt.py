# ******************************************
#  Author : Ali Azhari 
#  Created On : Sat Jun 29 2019
#  File : crypt.py
# *******************************************/
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

from utilities.errors import *


class Crypt:

    def __init__(self, key, salt):
        self.salt = salt
        self.key = key
        self.crypt_method = 'utf-8'

    def encrypt(self, string_to_encrypt):
        try:
            aes = AES.new(self.key, AES.MODE_CFB, self.salt)
            aes_encrypt = aes.encrypt(string_to_encrypt)
            encoded = b64encode(aes_encrypt).decode(self.crypt_method)
            return encoded
        except ValueError:
            raise EncryptionException('*** Encryption Error ***')

        return encoded


    def decrypt(self, string_to_decode):
        try:
            aes = AES.new(self.key, AES.MODE_CFB, self.salt)
            temp = b64decode(string_to_decode.encode(self.crypt_method))
            str_dec = aes.decrypt(temp)
            decoded = str_dec.decode(self.crypt_method)
        except ValueError:
            # print('Error occured in decryption: Check your password again..')
            raise DecryptionException('*** Decryption Error ***')

        return decoded

