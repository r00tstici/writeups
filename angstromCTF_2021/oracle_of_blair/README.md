# Oracle Of Blair - angstromCTF 2021

- Category: Crypto
- Points: 160
- Solves: 137

## Description

Not to be confused with the ORACLE of Blair.

`nc crypto.2021.chall.actf.co 21112`

Author: lamchcl

## Solution

We are given the source of a remote service that takes our input, substitutes `{}` (if present) with the flag and "encrypts" it with `AES` in `CBC` mode, using a random `key` generated at the beginning, an `IV` that changes for every input and the `decrypt function`!

Because it uses the decrypt function instead of the encrypt one, the `IV` is XORed only with the first block and doesn't affect the other ones. Furthermore a block of our input is XORed with the next block after the decryption, but if we fill the first block with `00` it doesn't affect the next block.

![CBC decryption](images/CBC_decryption.png "CBC decryption")

Then we found the flag's length by adding a character per time until the output contains another block: 25 characters.

After that analysis we ended up using a simple script to automate an `ECB oracle attack` that skips the first block and we found the flag: `actf{cbc_more_like_ecb_c}`

```python
BLOCK_SIZE = 16
FLAG_SIZE = 2 * BLOCK_SIZE - 7

flag = ""

for x in range(2*BLOCK_SIZE):
    c.recvuntil("give input: ", drop=True)
    c.sendline("00" * (2 * BLOCK_SIZE - x - 1) + "7b7d") #7b7d is the hex for {}
    decrypted = c.recvline().strip()
    decrypted_second_block = decrypted[2*BLOCK_SIZE:4*BLOCK_SIZE]

    for i in printable:
        i_hex = '{:02X}'.format(ord(i))

        c.recvuntil("give input: ", drop=True)
        payload = "00" * (2 * BLOCK_SIZE - x - 1) + \
            hexlify(flag.encode()).decode() + i_hex
        print(payload)
        c.sendline(payload)

        found = c.recvline().strip()
        found_second_block = found[2*BLOCK_SIZE:4*BLOCK_SIZE]

        if decrypted_second_block == found_second_block:
            flag += i
            print(flag)
            break
```

**Full script in https://github.com/r00tstici/writeups/blob/master/angstromCTF_2021/oracle_of_blair/exploit.py**
