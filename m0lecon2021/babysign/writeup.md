# Babysign

- Category: Crypto, warmup
- Points: 88
- Solves: 71
- Solved by: 4cu1, mcf1y

## Description
```
It's just a warmup, don't take it too seriously.

nc challs.m0lecon.it 7012
```

## Solution

We are provided with the following server.py file

```
from secret import flag
from Crypto.Util.number import bytes_to_long, getStrongPrime, inverse
from hashlib import sha256
import os

def prepare(m):
    if len(m)>64:
        m = m[:64]
    elif len(m)<64:
        l = 64-len(m)
        m = m + os.urandom(l)
    assert len(m) == 64
    return (m[:32],m[32:])

def sign(m,n,d):
    sign = pow(bytes_to_long(sha256(m[1]).digest())^bytes_to_long(m[0]), d, n)
    return hex(sign)[2:]

#doesn't even work, lol
def verify(m,s,n,e):
    return pow(int(s,16),e,n) == bytes_to_long(sha256(m[1]).digest())^bytes_to_long(m[0])

p,q = getStrongPrime(1024), getStrongPrime(1024)
n = p*q
e = 65537
d = inverse(e, (p-1)*(q-1))

while True:
    print()
    print("1. Sign")
    print("2. Sign but better")
    print("3. Verify")
    print("4. See key")
    print("0. Exit")
    c = int(input("> "))
    if c == 0:
        break
    elif c == 1:
        msg = input("> ").encode()
        print(sign(prepare(msg),n,d))
    elif c == 2:
        msg = input("> ").encode()
        print(sign(prepare(flag+msg),n,d))
    elif c == 3:
        msg = input("> ").encode()
        s = input("> ")
        print(verify(prepare(msg),s,n,e))
    elif c == 4:
        print("N:",n)
        print("e:",e)
    else:
        print("plz don't hack")
        break
```
We immediately notice the comment "doesn't even work, lol" and after a quick analysis of the code we concluded that it is possible to get the flag by executing the xor operation between the hash of the second block and the server response from the "Sign but better" mode. This obviously only in the case in which the flag is all contained in the first block.

We immediately carry out this check through the following logic:

In "Sign but better" mode the input is chained to the flag.
From the prepare function we can see that if flag+input has a length less than 64, random bytes are added up to bring the length to 64.

We begin to concatenate a character (in this case 'a').
All subsequent characters will be added randomly until reaching the length of 64.
Using this we can iterate over the number of chained characters, give the same input twice and check when the answer will be the same. In that case no random characters will be added and you will have flag + msg = 64.
The script satisfies this condition at the 39th iteration then we can get the length of the flag by subtracting the padding length from 64 (64 - 39 = 25).

We wrote the following script:
```
from pwn import *
import hashlib
import binascii

conn = remote("challs.m0lecon.it",7012)

# Proof of work
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
```

At this point we know that the flag is all contained in the first block.
We relaunch the service and in the 'Sign but better' mode we insert the character 'a' repeated 39 times.
We now have full control over the second block and we know that it is made up of the last 32 characters of the 39 we entered as input (all a). Consequently we can calculate the hash.

We save the server response and the public key values ​​that we will need to decrypt the text in the final step. In this case we have:

```
sign = "96dda6809da7e63c878f25b9913351724d2218fdfb00db8c7813b9eca28bbc412a999372edef8807bc9da07ce4a6c8e862534d34eda7b62b2fc222d490350e3bc4832c92052d1bf003919482a7c942cf15aa1305c5fa70b1c831447a0a855defb184a87338ee50f709b0084f4f35e7726a0b9b312ba2040bcfd9987d032e80212df47748837de9b399634ed051f669fcc0df5c87d341aa2e65cba8aae4a3a95110087ac8d0ea219a9f9e72a96dd2eaf4d9581654a0e459354161925188479ba7c7327e249208e64e1fee8361188b062b1c4d4899d6c65d84c9993c0331ccbdb19aadaee4299deaf128d768c752928bc7a7917864213a0843593309beb2d6ab72"

n = 20982048759418401556630465073837929724262663276404791358782187425047479093551594455225014206888800987050561844638476774976222559425477065735907185785006124267228230769281724626600354370064221519728627924293020690693296171612672293898584156770067953439676423656821176906957617753651608066415629581582844492536899862821333839319300127008382712317653349029649412261691581940160612667408839204601119933768223170743796525520202311699309433076868942277105347138707996574771466554543998080535996745456425206161291086580132024860330626595161207413253890218228514385883938655532924944193561924809674529159301162206351194215351

e = 65537
```
Now let's calculate the hash of the second block consisting of all a's and then apply the following formula in reverse to derive the first block.
```
pow(int(s,16),e,n) == bytes_to_long(sha256(m[1]).digest())^bytes_to_long(m[0])
```

At this point we can perform the calculation locally by replacing sign, e, n and the digest of the second block. Then we do the xor.

With the following code we can get the content of the first block that gives us the flag and part of our input.

```
from Crypto.Util.number import bytes_to_long
from hashlib import sha256
import binascii

sign = "96dda6809da7e63c878f25b9913351724d2218fdfb00db8c7813b9eca28bbc412a999372edef8807bc9da07ce4a6c8e862534d34eda7b62b2fc222d490350e3bc4832c92052d1bf003919482a7c942cf15aa1305c5fa70b1c831447a0a855defb184a87338ee50f709b0084f4f35e7726a0b9b312ba2040bcfd9987d032e80212df47748837de9b399634ed051f669fcc0df5c87d341aa2e65cba8aae4a3a95110087ac8d0ea219a9f9e72a96dd2eaf4d9581654a0e459354161925188479ba7c7327e249208e64e1fee8361188b062b1c4d4899d6c65d84c9993c0331ccbdb19aadaee4299deaf128d768c752928bc7a7917864213a0843593309beb2d6ab72"

n = 20982048759418401556630465073837929724262663276404791358782187425047479093551594455225014206888800987050561844638476774976222559425477065735907185785006124267228230769281724626600354370064221519728627924293020690693296171612672293898584156770067953439676423656821176906957617753651608066415629581582844492536899862821333839319300127008382712317653349029649412261691581940160612667408839204601119933768223170743796525520202311699309433076868942277105347138707996574771466554543998080535996745456425206161291086580132024860330626595161207413253890218228514385883938655532924944193561924809674529159301162206351194215351
e = 65537

a1 = pow(int(sign,16),e,n)

# Computation of the hash of the second block
m = "a"*32
hashed = bytes_to_long(sha256(m.encode()).digest())

# xor
flag = hashed^a1

print(binascii.unhexlify(hex(flag)[2:]).decode())

```

## Flag
`ptm{n07_3v3n_4_ch4ll3n63}`