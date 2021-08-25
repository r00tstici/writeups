## DIVIDING SECRETS

* category: crypto
* points: 434
* solves: 121
* solved by: mcf1y

### DESCRIPTION

challenge gives us the source code of server:

```python

from Crypto.Util.number import bytes_to_long, getStrongPrime
from random import randrange
from secret import flag

LIMIT = 64

def gen():
	p = getStrongPrime(512)
	g = randrange(1, p)
	return g, p

def main():
	g, p = gen()
	print("g:", str(g))
	print("p:", str(p))
	x = bytes_to_long(flag)
	enc = pow(g, x, p)
	print("encrypted flag:", str(enc))
	ctr = 0
	while ctr < LIMIT:
		try:
			div = int(input("give me a number> "))
			print(pow(g, x // div, p))
			ctr += 1
		except:
			print("whoops..")
			return
	print("no more tries left... bye")

main()	

```

When the connection starts, one prime number of 512 bits and a random number between 1 and *p* are generated, these two values are used to encrypt the flag.

The only thing we can do is give to the server a number to divide the flag value, the resulting value is encrypted and printed.

*MAIN OBSERVATION:* if div value is higher than x the resulting value of encryption is 1.

### SOLUTION:

We can find the exact value of *x* by using a binary search, infact if we give to the server a huge number bigger than x, it gives us 1, so we know that we have to search x in lower numbers, instead if the output isn't 1,so x is bigger than our input. Binary search is an algoritm that allows us do this search very quickly because discard many wrong possibilities.

### EXPLOIT:

```python

from pwn import *
from decimal import Decimal, getcontext
from Crypto.Util.number import long_to_bytes
import random

getcontext().prec = 500

k = random.getrandbits(512)

start = 0
end = k
ans = 0

while True:
    conn = remote("crypto.be.ax",6000)
    for _  in range(64):
        conn.recvuntil("number> ")

        mid = int(Decimal(start+end)/Decimal(2))
        
        conn.sendline(str(mid))
        
        res = conn.recvline().decode().strip()
        
        if res == "1":
            end = mid - 1
        else:
            start = mid + 1
            ans = mid
    print(long_to_bytes(ans))
    conn.close()

```

**FLAG: corctf{qu4drat1c_r3s1due_0r_n0t_1s_7h3_qu3st1on8852042051e57492}**

