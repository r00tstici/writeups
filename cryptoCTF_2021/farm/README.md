# Farm - cryptoCTF 2021

- Category: Crypto
- Points: 41
- Solves: 149
- Solved by: drw0if

## Description

Explore the Farm very carefully!

## Solution

In this challenge we were given two text files:
- farm.py: a sagemath script that generates a key and encrypts the flag
- enc.txt: the encrypted flag yelds by the previous script

First thing first: we are dealing with `Galois finite field` since the scripts creates this global object:
```python
F = list(GF(64))
```

Let's see the key generation:
```python
def keygen(l):
	key = [F[randint(1, 63)] for _ in range(l)] 
	key = math.prod(key) # Optimization the key length :D
	return key
```

At the end of the function we are given a single value in `GF(64)` but this field has only 64 values so we can brute-force the key.

We have to inverse the encryption function and we can go:
```python
    for c in enc:
        x = ALPHABET.index(c)       # c = ALHPABET[x]
        y = F[x]                    # x = F.index(y)
        z = farmtomap(y/pkey)       # y = pkey * maptofarm(z)
        m += z
```

At the end the flag was:
```
CCTF{EnCrYp7I0n_4nD_5u8STitUtIn9_iN_Fi3Ld!}
```
