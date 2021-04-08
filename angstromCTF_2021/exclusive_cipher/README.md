# Exclusive Cipher - angstromCTF 2021

- Category: Crypto
- Points: 40
- Solves: 499

## Description

Clam decided to return to classic cryptography and revisit the XOR cipher! Here's some hex encoded ciphertext:

`ae27eb3a148c3cf031079921ea3315cd27eb7d02882bf724169921eb3a469920e07d0b883bf63c018869a5090e8868e331078a68ec2e468c2bf13b1d9a20ea0208882de12e398c2df60211852deb021f823dda35079b2dda25099f35ab7d218227e17d0a982bee7d098368f13503cd27f135039f68e62f1f9d3cea7c`
The key is 5 bytes long and the flag is somewhere in the message.

Author: aplet123

## Solution

We could have brute-forced the key but knowing it is 5 characters long we knew it would take too long.

To make it faster we first found all the keys that give rise to a plaintext of printable characters only.

```python
possible_key_characters = []

for i in range(KEY_LENGTH):
    input_bytes_group = input_bytes[i::5]
    valid_keys_for_character = []

    for n in range(256):
        if all(chr(n ^ byte) in printable for byte in input_bytes_group):
            valid_keys_for_character.append(n)
    possible_key_characters.append(valid_keys_for_character)

keys = product(*possible_key_characters)
```

Only then we did the brute-force attack which turned out to be very fast.

```python
for k in keys:
    m = [chr(a ^ b) for a, b in zip(input_bytes, cycle(k))]
    plain = "".join(m)
    if "actf" in plain:
        print(plain)
```

One of the keys gave us the flag: `actf{who_needs_aes_when_you_have_xor}`

**Full script in https://github.com/r00tstici/writeups/blob/master/angstromCTF_2021/exclusive_cipher/exploit.py**
