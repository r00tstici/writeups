# Bootless RSA - DaVinciCTF

- Category: Crypto
- Points: 25
- Solves: 127
- Solved by: Crypt3d4ta, 4cu1

## Solution

We have JSON file in which we found:

- N = 148818474926605063920889194160313225216327492347368329952620222220173505969004341728021623813340175402441807560635794342531823708335067243413446678485411066531733814714571491348985375389581214154895499404668547123130986872208497176485731000235899479072455273651103419116166704826517589143262273754343465721499
- e = 3
- ct = 4207289555943423943347752283361812551010483368240079114775648492647342981294466041851391508960558500182259304840957212211627194015260673748342757900843998300352612100260598133752360374373

We immediately notice that the ciphertext is small compared to N.
We also have a low public exponent.

So we can get the plaintext message by simply making the third root of the ciphertext.

For simplicity, we put the following expression on wolframalpha.com:

"4207289555943423943347752283361812551010483368240079114775648492647342981294466041851391508960558500182259304840957212211627194015260673748342757900843998300352612100260598133752360374373 ^ (1/3)"

and we obtain: "161436153337866397698230350131849911745245662937350542382627197"

Converting to base 16 results: "64764354467B5253345F6D3064756C305F696E66316E6974797D"

So now, converting to ascii we get "dvCTF{RS4_m0dul0_inf1nity}" 










