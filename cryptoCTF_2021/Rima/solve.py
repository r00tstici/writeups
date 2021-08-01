from Crypto.Util.number import *
import binascii

def to_base_5(n):
    s = ''
    while n:
        s = str(n % 5) + s
        n //= 5
    return s


def nextPrime(n):
    while True:
        n += (n % 2) + 1
        if isPrime(n):
            return n

with open('g.enc', 'rb') as f:
    g_file = f.read()
    g_long = bytes_to_long(g_file)

with open('h.enc', 'rb') as f:
    h_file = f.read()
    h_long = bytes_to_long(h_file)

g_base5 = to_base_5(g_long)
h_base5 = to_base_5(h_long)

g_digits = [x for x in g_base5]
h_digits = [x for x in h_base5]

def worker(flag_len, g, h):
    f_size = flag_len * 8
    a = nextPrime(f_size)
    b = nextPrime(a)
    c = nextPrime(f_size >> 2)

    print(f'ATTEMPT WITH: a:{a}, b:{b}, c:{c}')

    if len(g) < a * f_size + c:
        g = [0] * (a*f_size+c - len(g)) + g

    if len(h) < b * f_size + c:
        h = [0] * (b*f_size+c - len(h)) + h

    g = [int(x) for x in g]
    h = [int(x) for x in h]

    for i in range(len(g) -  c -1, -1, -1):
        g[i] -= g[i+c]

    for i in range(len(h) -  c -1, -1, -1):
        h[i] -= h[i+c]

    if g[:c] != [0] * c or h[:c] != [0] * c:
        print('WRONG PADDING')
        print(f'WRONG LEN: {flag_len}')
        return

    g = g[c:]
    h = h[c:]

    g = g[:f_size]
    h = h[:f_size]

    if g != h:
        print('WRONG TRANSLATION')
        print(f'WRONG LEN: {flag_len}')

    f = g

    for i in range(len(f)-1-1, -1, -1):
        f[i] -= f[i+1]

    f = [str(x) for x in f]

    f = int(''.join(f), 2)
    f = hex(f)[2:]
    print(f'MAYBE FLAG: {f}')

    try:
        print(f'FLAG: {binascii.unhexlify(f)}')
    except:
        print('BAD HEX')

for i in range(50):
    worker(i, g_digits.copy(), h_digits.copy())
