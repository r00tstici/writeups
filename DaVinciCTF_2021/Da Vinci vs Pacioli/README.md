# Da Vinci vs Pacioli - DaVinciCTF

- Category: Stega
- Points: 74
- Solves: 18
- Solved by: 4cu1, hdesk, M4tex00

## Description

```
What an amazing game. Can you find my passwords?

Flag format: dvCTF{password}
```

## Solution

In this challenge we are given a zip file called 'important_files'.
Once the content has been extracted, we are faced with another zip and a file with the .pgn (Portable Game Notation) extension, a format used to record chess games.
The 'chest.zip' file is password protected. First we look in the 'amazing_game.pgn' file and try to get some more information.

```
[Event "Playing chess between drawings"]
[Date "2021.02.28"]
[White "Leonardo Da Vinci"]
[Black "Luca Pacioli"]
[Result "0-1"]
[UTCDate "1489.02.28"]
[UTCTime "11:35:18"]
[Variant "Standard"]
[TimeControl "-"]
[ECO "A00"]
[Opening "Anderssen Opening"]
[Termination "Normal"]

1. d4 { A40 Queen's Pawn Game } h5 2. g3 Rh7 3. b3 f6 4. Bh6 Kf7 5. Nc3 a5 6. Bh3 Qe8 7. a4 Kg6 8. f4 Kf7 9. e4 Na6 10. Nce2 Nb4 
2. 11. Rb1 Qd8 12. Kf1 Na2 13. c4 Nc3 14. Qc2 d6 15. Bxg7 Rxg7 16. Bf5 Ra7 17. h3 Rg4 18. Bg6+ Rxg6 19. Rb2 d5 20. Kg2 Qd7 
3. 21. Qc1 Ke6 22. b4 Nb1 23. Qd2 Nxd2 24. Rb3 Nh6 25. Kh2 dxc4 26. Re3 h4 27. gxh4 Nb1 28. Nf3 { Black resigns. } 1-0

```

We know that is possible to encode and decode data in a chess game via chess steganography.

Using the following site: `https://incoherency.co.uk/chess-steg` we can decode the moves of the game and get the string `3nfW@XuAT4LS4B5HmWBD&qMM5@RqVMgs` which turns out to be the zip archive password.

At this point we can extract the contents of the chest.zip file. We get two files: `keys.kdbx` and `nothing_to_see_here`.

To access the encrypted database we need a master password.

Even though the file is called "nothing to see here" we still tried to take a look. Also because the file has a large size.
The output of the command `strings nothing_to_see_here` appears to return a repeating pattern.

```
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ 

and so on.
```

To better analyze the content we redirect the output to a file with `strings nothing_to_see_here > out.txt`
Let's try to find out if there is something different from the usual pattern.
By running `sort -u out.txt > out2.txt` followed by `cat out2.txt` we obtain:

```
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
737570345f647570345f70347373773072645f346d347a316e675f6e30315f77316c6c5f73757370336374
```

As we suspected!
By converting the hexadecimal string we get the database master password: `sup4_dup4_p4ssw0rd_4m4z1ng_n01_w1ll_susp3ct`

Now we can access the database. Inside we found various accounts with their passwords. From the description of the challenge we know that a password must be entered between the flag format.
After few attemps we find the right one that corresponds to `MQNFZ0VPGDsfeQCvudeX`.
We put in the flag format, sent it and BOOM!, we got the points.

# Flag
`dvCVTF{MQNFZ0VPGDsfeQCvudeX}`
