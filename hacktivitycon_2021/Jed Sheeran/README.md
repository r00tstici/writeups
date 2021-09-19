# Jed Sheeran - hacktivitycon 2021

- Category: OSINT
- Points: 50
- Solves: 514
- Solved by: Iregon, crypt3d4ta

## Description

Oh we have another fan with a budding music career! Jed Sheeran is seemingly trying to produce new songs based off of his number one favorite artist... but it doesn't all sound so good. Can you find him?

**Find the flag somewhere in the world wide web with the clues provided.**

## Solution

First of all, we can try to search on Google for anything releated to Jed Sheeran and the music.

One of the first results is a link to SoundCloud:

![search](images/search.png)

Opening it we can see for first a "song" named `Beautiful People`. If we play it we can ear somthing similar to an old modem sounds.

![song](images/song.png)

For first we have start find what type of encoding is it but, luckly, we opened the song page and see the flag in the description:

![description](images/description.png)

## Flag

```
flag{59e56590445321ccefb4d91bba61f16c}
```
