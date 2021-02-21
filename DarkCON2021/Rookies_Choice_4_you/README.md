# Rookie's_Choice_4_you - DarkCON 2021

---

Category: Crypto
Points: 467
Solves: 51
Solved by: RxThorn

---

## Solution

In this challenge we are provided with a script and the output of the conversation of a user with this service.

In this conversation we get the encrypted flag and the encryption of some known messages. Looking at the script we see that the used key is the same.

The script uses `ARC4`, a stream cipher that generates a `keystream` (a string of pseudo-random numbers) and XORes that with the plaintext.

Even though we don't know the key used to generate the keystream, we can get that by reversing the XOR with a `known plaintext attack`. Indeed by xoring one of the encrypted string with its original message it is possible to obtain the keystream with which it was XORed.

```
0000000000000000000000000000000000000000000000000000000 (ASCII, Known plaintext)
XOR
6c0fd74818a4542dd8d35d5126fbb044218b4ceaebcf4a8e6895e431f36890a17f8c7ecef5d6554e706727eeafa062b58119068d8e15b3 (HEX, Known ciphertext)
=
5c3fe7782894641de8e36d6116cb807411bb7cdadbff7abe58a5d401c358a0914fbc4efec5e6657e405717de9f905285b12936bdbe2583 (HEX, Keystream)

385e95136bdb2a66baa0593e27b8df03228f1785ea9925c768d08b74b06bffe27bd17da1aed51c21342026bdacb173f8 (HEX, Encrypted flag)
XOR
5c3fe7782894641de8e36d6116cb807411bb7cdadbff7abe58a5d401c358a0914fbc4efec5e6657e405717de9f905285b12936bdbe2583 (HEX, Keystream)
=
darkCON{RC4_1s_w34k_1f_y0u_us3_s4m3_k3y_tw1c3!!}

```
