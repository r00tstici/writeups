# Read - DaVinciCTF

- Category: Web
- Points: 10
- Solves: 266
- Solved by: Lu191

## Description

Can you find a way to authenticate as admin?

`http://challs.dvc.tf:1337/`

## Analysis

The name of the challenge tells us that we need a way to authenticate as admin, so as we don't know the password we have to bypass the in some way authentication, the most common attack that we can try on this login page is a SQL Injection.

## Solution

The most common attack that we can try on this login page to bypass authentication is SQL Injection.
We try to login with the username `admin` and the password `' or 1 -- -` and we succeed we successfully bypassed authentication with a SQL Injection.
Now lets find the flag, let's inspect the code of the page where we have been redirected and indeed we find the flag.

## Flag

`dvCTF{!th4t_w4s_34sy!}`
