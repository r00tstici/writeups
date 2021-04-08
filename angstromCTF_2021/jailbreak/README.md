# jailbreak - angstromCTF 2021

- Category: Reverse
- Points: 75
- Solves: 218
- Solved by: drw0if

## Description

Clam was arguing with kmh about whether including 20 pyjails in a ctf is really a good idea, and kmh got fed up and locked clam in a jail with a python! Can you help clam escape?

Find it on the shell server at `/problems/2021/jailbreak` over over netcat at `nc shell.actf.co 21701`.

## Solution
We were given a [64 bit binary](dist\jailbreak) which consist of a basic text adventure in which we have to move our player through some kind of maze with some snake content, I dunno, I'm unable to read.

I started analyzing the source with ghidra and after a bit of "dude what the fuck" I reached a function whose purpose is to decode some string and print it. I wrote a [script](dist\extract.py) to patch the binary and print all of [them](dist\strings.txt) in order to add comment on ghidra for each of these function call.

Then I started with the real reversing trying to understand the logic. I got notes for each variable used as check and reached the following order:

```
check_1 = 0
check_2 = 1
check_3 = 0

pick the snake up
	-> tmp = 1
	-> You pick the snake up
	-> check_3 = 1

throw the snake at kmh
	-> tmp = 1
	-> You throw the snake at kmh and watch as he runs in fear.
	-> check_2 = 0
	-> check_3 = 1

pry the bars open
	-> check_1 = 1
	-> You start prying the prison bars open. A wide gap opens and you slip through.
```

to bypass the next check we are asked to build 0x539 into `check1` variable. The code provides us two primitives:

```
press the red button ->
	check_1 *= 2
	pos = 0x15

press the green button ->
	check_1 = check_1 * 2 + 1
	pos = 0x16
```

With red button we can add a 0 at the end of check1, with green button we can add a 1 at the end of it. So in binary we must build: `0x539 -> 10100111001` that can be forged with:

```
press the red button
press the green button
press the red button
press the red button
press the green button
press the green button
press the green button
press the red button
press the red button
press the green button
```
in the end we need to send `bananarama` and we get the flag.

```
actf{guess_kmh_still_has_unintended_solutions}
```