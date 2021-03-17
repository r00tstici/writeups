# Numbers - DaVinciCTF

- Category: Scripting
- Points: 98
- Solvers: 25
- Solved by: Crypt3d4ta, 4cu1

## Description

`nc challs.dvc.tf 3096`

## Solution

When we try to connect to the service, the server show us this text:
`Let's play a game. If you can tell me what number I am thinking of, I will give you the flag.
What number am I thinking of?`

When we try to guess the number, the server throws out:
`Nice try! I was thinking of <random_number>`

We assumed that the number are generated with python random module based on Mersenne Twister, a pseudo random generator.
To solved this challenge we wrote this script that at the end it worked perfectly.

`from pwn import *
from mt19937predictor import MT19937Predictor

conn = remote('challs.dvc.tf',3096)
print(conn.recvline())

numbers = []

for i in range(624):
    print(i)
    conn.sendline('3') # or any other value
    answer = conn.recvline().decode('ascii')
    split_answer = answer.split(' ')
    number = int(split_answer[12])
    numbers.append(number)
    print(number)

print(numbers)

predictor = MT19937Predictor()
for i in numbers:
    predictor.setrandbits(i,32)

guess = predictor.getrandbits(32)
print(type(guess))
print(guess)
conn.sendline(str(guess))
print(conn.recvline())`

`flag: dvCTF{tw1st3d_numb3rs}`
