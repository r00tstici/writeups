# Quotebook - DaVinciCTF

- Category: Pwn
- Points: 499
- Solves: 15
- Solved by: drw0if - hdesk

## Description

I created this amazing service to store all my famous quotes. Can you get the flag?

`nc challs.dvc.tf 2222`

## Solution

Since we are given the source code we started analyzing the general beaviour of the service: we can manage a list of `quotes` which are composed of:
- content
- content size
- title
- title size
- function pointer to quote_write function
- function pointer to quote_read function

For each quote we add the service asks malloc a chunk of memory for the main struct (48 bytes), a chunk for the title and a chunk for the content, we can choose che size for both the title and the content, and it increments a global counter `book_ctr`. Whenever we delete a quote it decrements `book_ctr` and frees the specified struct number.

At a first look the service appears to be vulnerable to double free and use-after-free:
- if we have 10 quotes and we ask to delete the first one it gets freed but the counter decrements to 9, so we can now delete all the structs from 1 to 9, so we can free again the first quote;
- if we free the first struct and `book_ctr` is more than one we can modify the first struct again.

We started creating 10 quotes and deleting 1 and 2 so we could fill up the `fastbin` list. We created a new quote and listing them we discovered that the second and the last one were identical: the fastbin attack can be abused!

Next we looked for a way to gather arbitrary read/write: we thought about creating a quote whose content pointer points to a user specified address, to achieve this we chained:
- allocate 10 quotes
- free 1 and 2 in order
- create a new quote whose content size is the same as struct size

in this way we got a new struct which is the same as the second one but the content pointer points to the base of the first struct since we asked for same size chunks. With this memory layout writing onto the second quote content we can overwrite the first quote content `pointer` which is used for quote editing.

Next step is to leak some libc address like fgets so we can calculate the offset at which libc has been loaded and then the real address of `system`, in order to achieve this we need to overwrite the first struct content pointer to the fgets `GOT` entry, then we can read the content and leak the address to do our calculations.

We are almost done: we need a libc function called with our directly input:
- no `printf` or `puts` is called with our input
- `fgets` is used to read the menu option so if we overwrite it we can't control the program anymore
- `sscanf` seems to be the only useful function cause it is used with our direct input to parse it in the menu function

We overwrite the sscanf GOT entry with system and launched `/bin/sh`.

In the end the exploit:
- allocate then quotes
- delete quote 1 to populate fastbin
- delete quote 2 to populate fastbin
- create a new quote with `content_size` set to 48
- edit the quote 9 (or 2) to overwrite quote 1 content pointer to sscanf@got address
- display quote 1 content to leak sscanf real address
- calculate the offset and the real `system` address
- edit the quote 1 content to set `system` address instead of `sscanf`
- send `/bin/sh` command
- profit
