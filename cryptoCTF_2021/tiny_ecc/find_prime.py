from Crypto.Util.number import *
import subprocess

def is_valid(p):
    return isPrime(p) and p.bit_length() == 128 and isPrime(2*p+1)

while True:

    value = subprocess.check_output(['openssl', 'prime', '-generate', '-bits',' 128'])
    p = int(value)

    print(f'ATTEMPT: {p}')

    if is_valid(p):
        print(f'FOUND: {p}')
        exit()

