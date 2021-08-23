from Crypto.Util.number import isPrime

def nextPrime(n):
    while not isPrime(n):
        n = n + 1
    return n

def memfrob(s):
    return bytes([x ^ 42 for x in s])

def unrot_n(c, key):
    if ord('a') <= c <= ord('z'):
        return (c - ord('a') - key) % 26 + ord('a')
    elif ord('A') <= c <= ord('Z'):
        return (c - ord('A') - key) % 26 + ord('A')
    return c

flag = b'\x5f\x40\x5a\x15\x75\x45\x62\x53\x75\x46\x52\x43\x5f\x75\x50\x52\x75\x5f\x5c\x4f'
flag = memfrob(flag)
flag = bytearray(flag)

for i in range(len(flag)):
    key = i * 4
    key = nextPrime(key)
    flag[i] = unrot_n(flag[i], key)

flag = b'corctf{' + flag + b'}'
assert len(flag) == 0x1c
print(flag)