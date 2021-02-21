# Risk Security Analyst Alice Vs Eve - DarkCON 2021

---

Category: Crypto
Points: 488
Solves: 21
Solved by: RxThorn

---

```
La Casa De Tuple (L.C.D.T) is a Company in Spain which provides their own End-to-end encryption services and Alice got a job there. It was her first day and her boss told her to manage the secrets and encrypt the user data with their new End-to-end encryption system. You are Eve and you're hired to break into the system. Alice was so overconfident that she gave you everyone's keys. Can you break their new encryption system and read the chats?
```

## Solution

For this challenge we have Alice's public and private key, other people's public key and their encrypted messages.
One important thing is that all the keys have the same module, so if we are capable to break one of that keys we can break all of them!
For sure the easiest one to break is Alice's, indeed we know her private key, so `d`, and from `d` and `n` it is easy to recover `n`'s factors `p` and `q`.

It has been easy to find on the internet an algorithm to factorize `n` given `d`: https://www.di-mgt.com.au/rsa_factorize_n.html.
We replicated that algorithm in Python and let it run. It found the factors almost immediately (with g=2 in that algorithm).

```py3
p = 11591820199541996689109613653787526255588052136591796590965030492566464176562040269220119399461110340988231294335751866203503669710592217665562209443382247
q = 11635054504921733826196411324113633422484567025939176480557681377109499625813425045440075923029853047713076440712050521568931550034720072522577709065411181
```

With that done, we let `RsaCtfTool` to the rest: first we saved the encrypted chats in different files and then we let the tool do all the calculations to find `d` given `p`, `q` and `e`. It is simple to create a script that does that calculation, but RsaCtfTool is ready!

We got the flag while decrypting Charlie's message with `./RsaCtfTool.py -p 11591820199541996689109613653787526255588052136591796590965030492566464176562040269220119399461110340988231294335751866203503669710592217665562209443382247 -q 11635054504921733826196411324113633422484567025939176480557681377109499625813425045440075923029853047713076440712050521568931550034720072522577709065411181 -e 4294967297 --uncipherfile charlie.txt`

Flag: `darkCON{4m_I_n0t_supp0sed_t0_g1v3_d???}`
