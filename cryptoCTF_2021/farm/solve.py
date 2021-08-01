from sage.all import *
import string, base64, math

enc = "805c9GMYuD5RefTmabUNfS9N9YrkwbAbdZE0df91uCEytcoy9FDSbZ8Ay8jj"

ALPHABET = string.printable[:62] + '\\='

F = list(GF(64))

def farmtomap(f):
    assert f in F
    return ALPHABET[F.index(f)]

def decrypt(cipher, key):
    m, pkey = '', key**5 + key**3 + key**2 + 1

    if pkey == 0:
        return b''

    for c in enc:
        x = ALPHABET.index(c)       # c = ALHPABET[x]
        y = F[x]                    # x = F.index(y)
        z = farmtomap(y/pkey)       # y = pkey * maptofarm(z)
        m += z

    try:
        m = base64.b64decode(m)
    except:
        return b''

    return m


for f in F:
    m = decrypt(enc, f)
    if b'CCTF' in m:
        print(m)

"""
b'CCTF{EnCrYp7I0n_4nD_5u8STitUtIn9_iN_Fi3Ld!}'
"""