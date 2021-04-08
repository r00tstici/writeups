# Home Rolled Crypto - angstromCTF 2021

- Category: Crypto
- Points: 70
- Solves: 173

## Description
Aplet made his own block cipher! Can you break it?

`nc crypto.2021.chall.actf.co 21602`

Author: EvilMuffinHa

## Solution

We are given the source of a remote service. This service generates a random key for every connection and generates a cipher that does multiple `xor` and `logical and` to the input, based on that keys.

We can ask the service to encrypt our input with that cipher or try to obtain the flag if we are able to correctly encrypt a string that the server gives to us.

`xor` and `logical and` are bit-per-bit operations and, because that cipher doesn't perform any permutation, we know for sure that if the nth bit of two input messages is the same, also the nth bit of the output will be the same.

So we created a script that encrypts a block of only 1 and a block of only 0.

```python
rainbow_table = []
for payload in ["00", "FF"]:
    r.recvuntil("[2]? ", drop=True)
    r.sendline("1")
    r.recvuntil("encrypt: ", drop=True)
    r.sendline(payload * BLOCK_SIZE)
    response = r.recvline().decode().strip()

    n = int(response, 16)
    rainbow_table.append([int(digit)
                          for digit in bin(n)[2:].rjust(8*BLOCK_SIZE, "0")])
```

Then it tries to encrypt what the server gives to us by splitting the input in bits and (for each bit) if the nth bit is 1 it replaces it with the nth bit of the output that the server gave us when we asked to encrypt the block full of ones. If that bit had been zero it would have done the same thing but replacing it with the encryption result of the block of zeros.

```python
for i in range(10):
    r.recvuntil("Encrypt this: ", drop=True)

    question = r.recvline().decode().strip()
    blocks = [question[i*BLOCK_SIZE*2:(i+1)*BLOCK_SIZE*2]
              for i in range(len(question)//(BLOCK_SIZE*2))]

    answer = ""
    for block in blocks:
        enc = int(block, 16)
        enc_bits = [int(digit)
                    for digit in bin(enc)[2:].rjust(8*BLOCK_SIZE, "0")]
        dec_bits = []

        for x in range(8*BLOCK_SIZE):
            dec_bits.append(rainbow_table[enc_bits[x]][x])

        out = 0
        for bit in dec_bits:
            out = (out << 1) | bit

        answer += str(hex(out)[2:])

    r.sendline(answer)
r.interactive()
```

So we won the flag `actf{no_bit_shuffling_is_trivial}`

**Full script in https://github.com/r00tstici/writeups/blob/master/angstromCTF_2021/home_rolled_crypto/exploit.py**
