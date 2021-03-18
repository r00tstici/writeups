# Format me - DaVinciCTF

- Category: Pwn
- Points: 90
- Solves: 47
- Solved by: drw0if

## Description

`nc challs.dvc.tf 8888`

## Solution

When we connected to the service we reached a command line service which reverse the input we provide. Since the challenge name reminds us about format string we attempted to leak informations:
```
%x %d %x
```

No particular output is provided... Let's try to puts it in reverse order:
```
x% d% x%
```

Boom, format string exploit confirmed! We sprayed some `%{i}$s` to leak all the string pointed by stack values and we got the flag.