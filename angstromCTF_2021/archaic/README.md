# Archaic - ångstromCTF 2021

- Category: Misc
- Points: 50
- Solves: 870
- Solved by: raff01

## Description

The archaeological team at ångstromCTF has uncovered an archive from over 100 years ago! Can you read the contents?

Access the file at `/problems/2021/archaic/archive.tar.gz` on the shell server.

`Hint`: What is a .tar.gz file?

`Author`: kmh

## Analysis
In this challenge we're given an archive called `archive.tar.gz` and we have to get its content.
First of all let's see what it contains by giving the command `tar -tf archive.tar.gz` : the result will be `flag.txt`. So the flag is inside the archive. If we try to extract it by using the command `tar -xf archive.tar.gz flag.txt` the shell will say that the operation isn't permitted so we have to find another way to get the content of the archive without extracting it.


## Solution

Let's open the archive with `vim` by giving the following command `vim archive.tar.gz` : the flag will be printed!

## Flag
```
actf{thou_hast_uncovered_ye_ol_fleg}
```
