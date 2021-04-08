from pwn import *
import json
from tqdm import tqdm

p = remote('crypto.2021.chall.actf.co', 21601)
value = []

for i in tqdm(range(500)):
    p.recvuntil('>')
    p.sendline(f'{i}')
    p.recvuntil('>> ')
    value.append((i, int(p.recvline())))

with open('dump.txt', 'w') as f:
    f.write(json.dumps(value))
