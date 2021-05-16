from pwn import *
import hashlib
import binascii
from Crypto.Util.number import bytes_to_long
from hashlib import sha256

# Proof of work

conn = remote("challs.m0lecon.it",7012)
req = conn.recvline().split()
begin = req[6]
end = req[-1]
end = end[:-1]

to_send = ""

for i in range(1000000):
    
    temp = begin.decode() + str(i)
    m = hashlib.sha256()
    m.update(temp.encode())
    dig = binascii.hexlify(m.digest())

    if dig.decode().endswith(end.decode()):
        to_send = temp
        print("Found\n")
        break

conn.sendline(to_send)

# Discover flag length

conn.recvuntil("Exit")

ctrl = 0
flag_length = 0

for i in range(1,65):
    if ctrl:
        break
    print(i)
    to_match = ""
    for j in range(1,3):
        conn.sendline("2")
        temp = "a" * i
        conn.sendline(temp)
        conn.recvline()
        res = conn.recvline()
        conn.recvuntil("Exit")
        if to_match == "":
            to_match = res
        else:
            if to_match == res:
                flag_length = 64 - i
                print("\nflag length --> " + str(flag_length))
                ctrl = 1

# Take sign , e , n

conn.sendline("2")
conn.sendline("a"*(64-flag_length))
conn.recvline()
sign = conn.recvline().decode()
print("\nSign -> " + sign)
conn.recvuntil("Exit")
conn.sendline("4")
conn.recvline()
n = conn.recvline()
e = conn.recvline()
n = int(n.split()[1].decode())
e = int(e.split()[1].decode())

print("\nn -> " + str(n))
print("\ne -> " + str(e))

# Get the flag

a1 = pow(int(sign,16),e,n)

# Computation of the hash of the second block
m = "a"*32
hashed = bytes_to_long(sha256(m.encode()).digest())

# xor
flag = hashed^a1

print("\n\nFLAG")
print(binascii.unhexlify(hex(flag)[2:]).decode())