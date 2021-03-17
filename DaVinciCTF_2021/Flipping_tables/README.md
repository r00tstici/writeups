# Members - DaVinciCTF

- Category: Crypto
- Points: 73
- Solves: 23
- Solved by: SM_SC2, 0xThorn, Th3Revenge

## Description

┳━┳ ヽ(ಠل͜ಠ)ﾉ

`nc challs.dvc.tf 3333`


## Analysis

The challenge accepts a hex string and prints a custom hash. The most important thing we have to note is that it prints two different answers: `E(input || flag)` and `!E(input || flag)`. We decided to ignore `!E(input || flag)` answer and to understand what `E(input || flag)` means.
So we started to insert a lot of string of different length and to take note of every result.

|   Input  |                                                                        E(input \|\| flag)                                                                        | Length |
|:--------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------:|--------|
|          | 7caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09                                                                                                 | 64     |
| '0' * 2  | a680be8ae7921f855290508120d8f2f06bc1563491713fa0c2f76f0fbbb799d9                                                                                                 | 64     |
| '0' * 4  | e6de7a0fbed3f07fa8069390484814b8322b94a315b8f8ad9329a3df83ee4099                                                                                                 | 64     |
| '0' * 8  | f9952c4d157bac9a94dcb4bd01ad8893d7a39d11517c8ffc12adeb2d60e1b12c                                                                                                 | 64     |
| '0' * 16 | d26b8b947a906dee1875d7c47f3fd830fb08b408dcc9910df47f90788438186d                                                                                                 | 64     |
| '0' * 32 | 001f11041f67ed07b61b191f997498167caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09                                                                 | 96     |
| '0' * 18 | b9d0828cdfd56526f1c5db5800cee3ea18f77807d91f685f7c9ec14b59a479d9155075db7f6ceeafd3d4db2a44eae980                                                                 | 96     |
| '0' * 64 | 001f11041f67ed07b61b191f99749816001f11041f67ed07b61b191f997498167caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09                                 | 128    |
| '0' * 48 | 001f11041f67ed07b61b191f99749816d26b8b947a906dee1875d7c47f3fd830fb08b408dcc9910df47f90788438186d                                                                 | 96     |
| '0' * 50 | 001f11041f67ed07b61b191f99749816b9d0828cdfd56526f1c5db5800cee3ea18f77807d91f685f7c9ec14b59a479d9155075db7f6ceeafd3d4db2a44eae980                                 | 128    |
| '0' * 80 | 001f11041f67ed07b61b191f99749816001f11041f67ed07b61b191f99749816d26b8b947a906dee1875d7c47f3fd830fb08b408dcc9910df47f90788438186d                                 | 128    |
| '0' * 82 | 001f11041f67ed07b61b191f99749816001f11041f67ed07b61b191f99749816b9d0828cdfd56526f1c5db5800cee3ea18f77807d91f685f7c9ec14b59a479d9155075db7f6ceeafd3d4db2a44eae980 | 160    |


We can see that hash length is a multiple of 32 characters.

| Input length | Hash Length |
|:------------:|------------------|
| 0            | 64               |
| 16           | 64               |
| 18           | 96               |
| 48           | 96               |
| 80           | 128              |
| 82           | 160              |

Comparing `'0' * 32`, `'0' * 50` and `'0' * 64` hashes we can see that the first 32 characters are the same.

**001f11041f67ed07b61b191f99749816**7caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09

**001f11041f67ed07b61b191f99749816**b9d0828cdfd56526f1c5db5800cee3ea18f77807d91f685f7c9ec14b59a479d9155075db7f6ceeafd3d4db2a44eae980

**001f11041f67ed07b61b191f99749816**001f11041f67ed07b61b191f997498167caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09

Comparing `empty input`, `'0' * 32`, `'0' * 64` and `'f'*64` hashes we can also see that the last 32 characters are the same.

**7caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09**

001f11041f67ed07b61b191f99749816
**7caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09**

001f11041f67ed07b61b191f99749816001f11041f67ed07b61b191f99749816
**7caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09**

0af5f8cd3f7077ca02eccd3f9ee840750af5f8cd3f7077ca02eccd3f9ee84075
**7caafa90873c58d4640dd8b9894c929ac908eab8b015d40fc92d62674716fc09**

So we understood that `E(input || flag)` means
1) Concatenate input with flag
2) Add padding if `len(input) < 32`
3) Encrypt

This is an `Oracle padding`.

## Solution

`BLOCK_SIZE = 32`

The idea is to brute force each character of the flag:
1) Send `'0' * (BLOCK_SIZE - 2)` and take note of the hash ( `encrypted_flag` )
2) For each printable character c, send `hex(c)` padded with `BLOCK_SIZE - 2` zeros and store the hash ( `encrypted_char` )
3) If `encrypted_flag == encrypted_char` we found the first character
4) Reduce padding of 2 characters and append `encrypted_flag`
5) Repeat until you complete first block

We have the first part of the flag `'dvCTF{3CB_4ngry_'`.
Now we have to change `BLOCK_SIZE` to 64 characters and repeat all using the first part of hashed flag.

To be sure that the idea was good, we first compared `'0' * 30` hash with `'0' * 30 + 'd'` hash as we knew that the flag should have started with `d`


## Flag

`dvCTF{3CB_4ngry_0r4cl3}`

