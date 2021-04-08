# I'm so Random - angstromCTF 2021

- Category: Crypto
- Points: 100
- Solves: 238

## Description

Aplet's quirky and unique so he made my own PRNG! It's not like the other PRNGs, its absolutely unbreakable!

`nc crypto.2021.chall.actf.co 21600`

Author: EvilMuffinHa

## Solution

In this challenge we are given the source of a remote service that generates some pseudo-random numbers and asks us to gess the following ones. We can ask three random numbers and then we have to guess.

At the beginning it creates two generators with some random seeds and the next numbers are generated in a deterministic way, based on the previous generated number.

```python
class Generator():
    DIGITS = 8
    def __init__(self, seed):
        self.seed = seed
        assert(len(str(self.seed)) == self.DIGITS)

    def getNum(self):
        self.seed = int(str(self.seed**2).rjust(self.DIGITS*2, "0")[self.DIGITS//2:self.DIGITS + self.DIGITS//2])
        return self.seed
```

When we ask for a number, the server gives us the product of the two random numbers obtained from the two generators.

Because the output we get is a product, we can factor it with FactorDB. Some of that primes are the factors of the first number and some of the second one. We can test all the cases and find which case allows us to generate correctly the next number.

```python
# Get three random numbers and factorize them
for i in range(3):
    r.recvuntil("[g]? ", drop=True)
    r.sendline("r")

    n = int(r.recvline().strip())

    f = FactorDB(n)
    f.connect()
    assert f.get_status() == "FF", "Number not factored"
    f = f.get_factor_list()

    got_numbers.append(n)
    got_factors.append(f)

# Find all possible seed couples
possible_second_seeds = []

first_factors = got_factors[0]
for p in product([0, 1], repeat=len(first_factors)):
    first_seeds=[1, 1]

    for i in range(len(first_factors)):
        first_seeds[p[i]] *= first_factors[i]

    if len(str(first_seeds[0])) == 8 and len(str(first_seeds[0])) == 8:

        second_seeds=get_seeds(first_seeds)

        if second_seeds[0] * second_seeds[1] == got_numbers[1]:
            possible_second_seeds.append(second_seeds)
```

Our script did that and had been able to find the right random numbers. Then it is easy to find the next random number by using the same function as the server does.

Flag: `actf{middle_square_method_more_like_middle_fail_method}`

**Full script in https://github.com/r00tstici/writeups/blob/master/angstromCTF_2021/im_so_random/exploit.py**
