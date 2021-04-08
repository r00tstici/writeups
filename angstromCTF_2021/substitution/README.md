# Substitution - angstromCTF 2021

- Category: Crypto
- Points: 130
- Solves: 135
- Solved by: drw0if

## Description
[Source](dist/chall.py)

`nc crypto.2021.chall.actf.co 21601`

## Solution

In this challenge we can interact with a netcat service that asks us integers and yelds the value of substitution function on our value. Analyzing the substitute function it computes:
```
def substitute(value):
    return (reduce(lambda x, y: x*value+y, key))%691
```

which basically means:
```
((((key[0] * value + key[1]) * value + key[2]) * value + key[3]) * value + key[4])... % 691
```

The first thing we attempted was to throw the expression with a lot of input values inside `z3-solver` but it was always UNSAT.

Then we started analyzing better the expression and reached this form:
```
key[0]*value^(n-1) + key[1]*value(n-2) + ... key[n-2]*value + key[n-1] mod 691
```

which is a polynom modulo prime number. Remembering the service we can get pair `<x, y>` so we can basically do a polynom interpolation and since the best fit polynom is unique we should find the right coefficients (the key values), but what to do about the module? Well when we work with a prime modulo we are playing in `Galois finite fields` which are fields so we can do all the basic operations like sum, substraction and more. The lagrange polynom interpolation indeed works in finite field so we can arrange a resolving script in `SageMath`:

```python
from sage.all import *

F = GF(691)

points = [
    [0, 125], [1, 492], [2, 670], [3, 39], [4, 244],
    [5, 257], [6, 104], [7, 615], [8, 129], [9, 520],
    [10, 428], [11, 599], [12, 404], [13, 468], [14, 465],
    [15, 523], [16, 345], [17, 44], [18, 425], [19, 515],
    [20, 116], [21, 120], [22, 515], [23, 283], [24, 651],
    [25, 199], [26, 69], [27, 388], [28, 319], [29, 410],
    [30, 133], [31, 267], [32, 215], [33, 352], [34, 521],
    [35, 270], [36, 629], [37, 564], [38, 662], [39, 640],
    [40, 352], [41, 351], [42, 481], [43, 103], [44, 161],
]

R = F['x']
f = R.lagrange_polynomial(points)
coeffs = f.coefficients()
print(''.join([chr(x) for x in coeffs])[::-1])
```

```
actf{polynomials_20a829322766642530cf69}
```