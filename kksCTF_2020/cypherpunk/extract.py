import sys
import re
import os

for l in os.listdir('downloaded'):
    with open(f'downloaded/{l}', 'r') as f:
        a = f.read()

    regex = r'(-----BEGIN PGP MESSAGE-----(.|\n)*-----END PGP MESSAGE-----)'
    result = re.findall(regex, a)

    with open(f'stripped/{l}', 'w') as f:
        f.write(result[0])

    print(l)
