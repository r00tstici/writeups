# Kanagawa - DaVinciCTF

- Category: Pwn
- Points: 59
- Solves: 92
- Solved by: drw0if - hdesk

## Description

`nc challs.dvc.tf 4444` or `nc challs.dvc.tf 7777`

## Solution

Common buffer overflow with jump to a never called function, since there is no PIE enabled we can spam the function address and hope to reach the target