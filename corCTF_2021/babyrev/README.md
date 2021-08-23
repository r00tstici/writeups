# babyrev - corCTF2021

- Category: Reverse
- Points: 372
- Solves: 203
- Solved by: drw0if

## Description

well uh... this is what you get when you make your web guy make a rev chall

## Solution

We are given an ELF binary, decompiling it with Ghidra it is fairly easy to spot a basic encryption algorithm:
- the provided string must start with `corctf{` and finish with `}`
- the full length must be 28 characters
- the flag content is copied into another buffer
- for each character of the string it gets the first prime number greater than `4 * character position`
- call `rot_n` function over the current character with the prime number calculated, it simply applies caesar encryption with the specified prime number as the key

In the end there is the actual comparison, it takes the global string `check` and passes it via `memfrob`.
That function simply applies xor encryption with the key `42`.
The last thing to do is to compare the encrypted user string with the xored one.

We can simply apply the reverse algorithm over the `check` string and recover the flag

```
corctf{see?_rEv_aint_so_bad}
```