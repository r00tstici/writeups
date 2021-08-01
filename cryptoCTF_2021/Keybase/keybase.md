# KEYBASE

*	Category: Crypto
*	Points: 48
*	Solves: 118
*	Solved by: mcf1y

## DESCRIPTION:

Recovering secrets is hard, but there is always some easy parts!

## ANALYSIS:

The challenge provides as the source code of the server:


```python

from Crypto.Util import number
from Crypto.Cipher import AES
import os, sys, random
from flag import flag

def keygen():
	iv, key = [os.urandom(16) for _ in '01']
	return iv, key

def encrypt(msg, iv, key):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.encrypt(msg)

def decrypt(enc, iv, key):
	aes = AES.new(key, AES.MODE_CBC, iv)
	return aes.decrypt(enc)

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

def main():
	border = "+"
	pr(border*72)
	pr(border, " hi all, welcome to the simple KEYBASE cryptography task, try to    ", border)
	pr(border, " decrypt the encrypted message and get the flag as a nice prize!    ", border)
	pr(border*72)

	iv, key = keygen()
	flag_enc = encrypt(flag, iv, key).hex()

	while True:
		pr("| Options: \n|\t[G]et the encrypted flag \n|\t[T]est the encryption \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'g':
			pr("| encrypt(flag) =", flag_enc)
		elif ans == 't':
			pr("| Please send your 32 bytes message to encrypt: ")
			msg_inp = sc()
			if len(msg_inp) == 32:
				enc = encrypt(msg_inp, iv, key).hex()
				r = random.randint(0, 4)
				s = 4 - r
				mask_key = key[:-2].hex() + '*' * 4
				mask_enc = enc[:r] + '*' * 28 + enc[32-s:]
				pr("| enc =", mask_enc)
				pr("| key =", mask_key)
			else:
				die("| SEND 32 BYTES MESSAGE :X")
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()

```

When we open the connection, we can perform two simple operations through the menu.

- [G]et The encrypted flag

- [T]est the encryption

The server uses AES CBC to encrypt, key and IV are generated only ones by the function **keygen()**

if we select the first option, the server gives us the encrypted flag.

instead if we select the second option, the server asks us a 32 byte message to encrypt and as output we have the first 14 bytes of the key and a part of the encrypted text, in fact we know only the whole second block and a few byte of the first.

the goal is to find key and IV to decrypt the flag.

## SOLUTION:

this is the decryption schema of AES CBC:

![](AES_CBC_decryption.png)

for testing i sent to the server this fake flag:

**CCTF{xxxxxxxxxxxxxxxxxxxxxxxxxx}**

* ciphertext1 --> first ciphertext block
* ciphertext2 --> second ciphertext block
* plaintext1 --> first plaintext block
* plaintext2 --> second plaintext block

#### Ask to the server the mask\_enc and the key\_enc:


```python
conn = remote("01.cr.yp.toc.tf", 17010)

conn.sendline(b"G")
conn.recvuntil(b"= ")
enc_flag = binascii.unhexlify(conn.recvline(False))


while True:
    conn.sendline(b"T")
    conn.sendline(b"CCTF{xxxxxxxxxxxxxxxxxxxxxxxxxx}")

    conn.recvuntil(b"enc = ")
    enc = conn.recvline(False)

    conn.recvuntil(b"key = ")
    key = conn.recvline(False)

    if b"*" not in enc[:4]:
        break

key = key[:-4].decode()
enc = enc.replace(b"*", b"0")
```

the number of known bytes of ciphertext1 is random and max 2, so i ask to decrypt the message until i get the first two bytes.

#### Find the key:

in this case the whole key is composed by 16 bytes, but we know only 14 of them, so we can bruteforce the other ones.
When the key is right, we obtain the first two characters of the second plaintext block.

```python
def bruteforce_key():
    keys = []
    for i in range(0,256):
        for j in range(0,256):
            b1 = hex(i)[2:].rjust(2, "0")
            b2 = hex(j)[2:].rjust(2, "0")
            k = key+b1+b2
            aes = AES.new(binascii.unhexlify(k), AES.MODE_CBC, cipher_block1)
            p = str(aes.decrypt(cipher_block2))[2:-1]
            if str(p).startswith("xx"):
                keys.append(binascii.unhexlify(k))
    return keys
```

#### Find the whole first ciphertext block:

The idea is that we can reverse the roles of the ciphertext1 and plaintext2 so that when the ciphertext2 is decrypted, is performed the xor operation with the known plaintext2 and we get the ciphertext1.

```python
def findCipher1(key):
    aes = AES.new(key, AES.MODE_CBC, plain_block2)
    return aes.decrypt(cipher_block2)
```

#### Find the IV:

To find the IV we can exploit the same idea, but this time we use plaintext1 as IV and than decrypt the ciphertext1 that we found.

```python
def findIV(key, cipher1):
    aes = AES.new(key, AES.MODE_CBC, plain_block1)
    return aes.decrypt(cipher1)
```


#### Decrypt the flag:

now we have all to decrypt the encrypted flag:

```python
keys = bruteforce_key()
for k in keys:
    cipher1 = findCipher1(k)
    IV = findIV(k, cipher1)
    aes = AES.new(k, AES.MODE_CBC, IV)
    flag = aes.decrypt(enc_flag)
```

flag: **CCTF{h0W_R3cOVER_7He_5eCrET_1V?}**








