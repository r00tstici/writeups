# Tony And James - DarkCON 2021

---

Category: Crypto
Points: 472
Solves: 45
Solved by: RxThorn

---

## Solution

For this challenge we had a pdf containing a dialogue between Mr. Tony Stark and his friend James. At the end of this file we have an interesting string: `r0 = 1251602129774106047963344349716052246200810608622833524786816688818258541877890956410282953590226589114551287285264273581561051261152783001366229253687592`.
We also have a python script and a text file containing the result of the encryption.

Let's analyze the script. In the beginning it calls the function `get_seed` which gets a random number as long in bits as the plaintext is in bytes. Then it creates an array `raw` containing all the possible `right shifts` of this number. The function returns the array `raw` and a number `seed` which is the sum of all the numbers contained in raw. This is interesting because if we know the first number container in raw, we can obtain all the other and therefore also seed.
It is important because `seed` is used as seed for the random function, so if we can obtain the seed we can also obtain the same random numbers he got.

Later it encrypts the message byte per byte with the XOR: `r ^ m[i] ^ raw[i]` where `m[i]` is the i-th letter of the plaintext and r is a random number calculated with `random.randint(1, 2**512)` for each letter. The result of each one of these operations is saved in the third file we have.

The first calculation is `F0 = r0 ^ m[0] ^ raw[0]`, where `F0` is in the output file, `r0` is the only r that we have which is in the PDF and `m[0]` is the first letter of the plaintext, which we know due to the flag format (d). At this point it is possible to calculate `raw[0] = F0 ^ r0 ^ m[0]`. Now that we know the first element of raw we can calculate all the others by shifting it and the sum all these values to obtain seed, give it to `rand` and obtain all the other `r` as the author did. At this point it is easy to obtain the plaintext given `ri, Fi, raw[i]` with `m[i] = ri ^ Fi ^ raw[i]`.

We wrote a Python script to do that and we have been able to obtain the flag: `darkCON{user_W4rm4ch1ne68_pass_W4RM4CH1N3R0X_t0ny_h4cked_4g41n!}`
