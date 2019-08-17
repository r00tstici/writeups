In this misc challenge with the description:
```
Win Tux Trivia Show!

nc chall2.2019.redpwn.net 6001
```

we were given a challenge to solve: the software prompt us for the capital of a State and we must provide it in time, for example:

```
$ nc chall2.2019.redpwn.net 6001
Welcome to Tux Trivia Show!!!
What is the capital of Italy?
Rome
Correct! Next question coming...
```

So the easiest thing is to create a script to play it and provide the city some web-scraping/hardcoding. After a while we will reach the end:

```
Correct! Next question coming...

Here is your flag: flag{TUX_tr1v1A_sh0w+m3st3r3d_:D}
```