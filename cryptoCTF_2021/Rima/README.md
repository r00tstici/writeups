# Rima - cryptoCTF2021

- Category: Crypto
- Points: 56
- Solves: 93
- Solved by: drw0if, RxThorn

## Description

Sequences are known to be good solutions, but are they good problems?

## Solution

In this challenge we were given 3 files:
- rima.py: the encryption algorithm
- g.enc: some binary encrypted stuff
- h.enc: some binary encrypted stuff

The encryption algorithm starts by getting the flag and parsing bit by bit. 
The result is the array `f`.
Then we insert a `0` element at the beginning of the list, this adjustment makes the array length a multiple of 8: since the first character of the flag is `C` it is parsed into only 7 bit, adding one we reach the 8 bit for each digit.

Then some additions, then we extract two adjacent prime numbers greater than the length of the list.

This esoteric python line:
```python
g, h = [[_ for i in range(x) for _ in f] for x in [a, b]]
```
can be rewritten as:
```python
g = f * a
h = f * b
```

Finally we extract another prime number and make some more insertion and additions.
In the end we convert each digit in the string representation, join the strings all togheter and parse the string as a base 5 number.
The number is then converted in a byte string and it is written to the two files.

The function `nextPrime(n)` search for the first prime greater than `n` so given the same `n` the result will always be the same.
Thus if we know the length of `f` we can recover all the prime numbers and invert the encryption.

Mine approach was to brute-force the length of the flag and thus the length of `f` and attempt the decryption, luckily we get the flag.

Another approach (thanks to RxThorn) was to calculate the flag length (indeed 32) and then apply the inverse function.

```
CCTF{_how_finD_7h1s_1z_s3cr3T?!}
```
