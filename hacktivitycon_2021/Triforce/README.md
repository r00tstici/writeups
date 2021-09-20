## TRIFORCE

- category: crypto
- points: 444
- solver: 73
- solved by: mcf1y, crypt3d4ta

### ANALYSIS:

we are provided of the source code of the server.



Basically at start the flag is splitted in three blocks of 16 bytes and you can choose which part use as key and IV (key and IV are equals). For example you can choose the first part of the flag as IV and key so plaintext is encrypted with them.

To encrypt is used AES with CBC as mode of operation, in this way:

```python

cipher = AES.new(self.triforce, AES.MODE_CBC, iv=self.triforce)

# self.triforce is one of [first_flag_block, second_flag_block, third_flag_block] and is choosen by user.

```

Also our plaintext is padded when we encrypt, but one important thing is that we don't get any error messages when we decrypt also if the padding is wrong

```python

def magic_padding(self, msg):
    val = 16 - (len(msg) % 16)
    if val == 0:
        val = 16
    pad_data = msg + (chr(val) * val)
    return pad_data

```


```python

def decrypt_sacred_saying(self, triforce):
    self.send("PLEASE ENTER YOUR SACRED SAYING IN HEXADECIMAL: ")

    saying = self.receive("decrypt> ")
    saying = binascii.unhexlify(saying)
    if (len(saying) % 16) != 0:
        self.send("THIS IS NOT A SACRED SAYING THAT THE GODS CAN UNDERSTAND")
        return
    cipher = AES.new(self.triforce, AES.MODE_CBC, iv=self.triforce)

    sacred = cipher.decrypt(saying)
    self.send("THANK YOU. THE GODS HAVE SPOKEN: ")
    self.send(binascii.hexlify(sacred).decode("utf-8") + "\n")


```

The goal is to choose one of the three flag blocks and recover the IV.

### SOLUTION:

This is the decryption schema of AES CBC. 

![](./AES_CBC.png)

Let's first consider the last block, we know that

```python

last_plain_block = D_k(last_cipher_block) ^ second_cipher_block

```

so we can calculate D_k(last_cipher_block) as

```python

D_k(last_cipher_block) = last_plain_block ^ second_cipher_block

```

If we send to the server a ciphertext with first block equals to the last block we have:

```python

D_k(first_cipher_block) = D_k(last_cipher_block)

```

but we know also that (this is valid for every selected flag block)

```python

first_plain_block = D_k(first_cipher_block) ^ first_flag_block

```

so at the end we have only xor D_k(first_cipher_block) with the first block of the plaintext

```python

first_flag_block = first_plain_block ^ D_k(first_cipher_block)

```

now we can iterate the process for every of the three flag blocks.

### EXPLOIT

```python

from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes

block = b'a'*32
dec_block = int(block, 16)
def find_flag(n, conn):
    conn.recvuntil(b"triforce# ")
    conn.sendline(str(n))
    conn.recvuntil(b"select# ")
    conn.sendline(b"2")
    conn.recvuntil("decrypt> ")
    conn.sendline(block*3)
    conn.recvuntil(b"SPOKEN: \n")
    cipher = conn.recvline().strip()
    dec_last_plain_block = int(cipher[-32:], 16)
    dec_first_plain_block = int(cipher[:32], 16)
    
    x = dec_last_plain_block ^ dec_block
    flag = x ^ dec_first_plain_block
    return long_to_bytes(flag)

conn = remote("challenge.ctf.games", 31084)
first_part = find_flag(1, conn)
conn = remote("challenge.ctf.games", 31084)
second_part = find_flag(2, conn)
conn = remote("challenge.ctf.games", 31084)
third_part = find_flag(3, conn)

print(first_part+second_part+third_part)

```

**FLAG: flag{819f9d8d83721ac4c442b1659f36df2d}**
