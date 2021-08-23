# Chainblock - corCTF

- Category: Pwn
- Points: 394
- Solves: 176
- Solved by: drw0if

## Description

I made a chain of blocks!

`nc pwn.be.ax 5000`

## Solution

We are given an ELF binary, its loader and its libc version.
We are also provided with the source code.
The vulnerable part is of course the use of the `gets` function wich leads to a basic buffer overflow. 
The binary has only the NX mitigation, so nothing avoid us to perform a ROP chain attack.
```bash
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x3fe000)
    RUNPATH:  b'./'
```

Since the binary has no win function and we are provided with the libc file, it is suggested that we have to perform a ret2libc attack.

First thing first we have to find the RIP offset from the start of the input buffer, we can basically crash the programm with a long enough input inside `gdb` and check the offset. It is `264`.

Next we have to leak a libc address to defeat the ASLR, we can jump to `printf@plt` and pass as parameter the address of `printf@got`.
Once we leaked the address we can calculate the libc base address.

After the leak we have to perform another buffer overflow, so let's jump to main and craft another ROP-chain. Now we just need to jump to system and pass the address of `/bin/sh` as parameter to the function.

Sometimes the rop-chain won't work because printf and system function crash.
That happens because the stack is not aligned to 16 byte, to fix this issue we can put a `ret gadget` as the first gadget, so it will pop 8 bytes from the stack and fix the alignment.


```
corctf{mi11i0nt0k3n_1s_n0t_a_scam_r1ght}
```