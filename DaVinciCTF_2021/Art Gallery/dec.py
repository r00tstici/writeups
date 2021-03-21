import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = key

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.decrypt(enc[AES.block_size:])

        
f = open('flag_sur_fond_de_soleil_couchant.jpg', 'rb')
enc = f.read()
f.close()
key = b"RLY_SECRET_KEY_!"
c = AESCipher(key)
dec = c.decrypt(enc)
g = open('dec.jpg', 'wb')
g.write(dec)
g.close()
