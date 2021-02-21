# Take It Easy - DarkCON 2021

- Category: Crypto
- Points: 428
- Solves: 99
- Solved by: RxThorn

## Solution

### Part 1

This challenge starts with an encrypted zip archive and a text file: `getkey.txt`.

The content of that file seemed like an RSA challenge where we were given p, ct and e.
We immediately notice that p is very large (and so does n) and e is very small.
The first try is to calculate the cube root of ct (`small e attach`) which is `351617240597289153278809` that, transformed into a string, is the key

```py3
>>> m = 351617240597289153278809
>>> mhex = hex(m)
>>> string = unhexlify(mhex[2:])
>>> print(string)
b'Ju5t_@_K3Y'
```

### Part 2

In the extracted archive there are a Python script and an output of that script.
That script divided the flag into blocks of 4 bytes and XORed the n-th block with the (n+2)-th one. Then printed the result in cipher.txt.
We knew the first two blocks due to the flag format (`darkCON{`), so we were able to calculate the 3rd block by doing `dark XOR B0` (the first row in cipher.txt) and the 4th one with `CON{ XOR B1`, and so on, because for example we now know the 3rd block and we can calculate the 5th one.

The script did it automatically and we got the flag: `darkCON{n0T_Th@t_haRd_r1Ght}`

> :warning: pack and unpack reversed the bytes order, so we had to reverse them again.
