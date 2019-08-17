In this crypto challenge with the following description:
```
Does hashing something multiple times make it more secure? I sure hope so. I've hashed my secret ten times with md5! Hopefully this makes up for the fact that my secret is really short. Wrap the secret in flag{}.

Note: Follow the format of the provided hash exactly

Hash: CD04302CBBD2E0EB259F53FAC7C57EE2
```
we were given an hash string to reverse but the problem is that this hash is the product of a 10 long hash chain, so it is the product of md5(md5(md5(...))). The only solution is to bruteforce it but we need some hint to avoid time waste. Reading further the description it says that the original string is *really* short, so we are allowed to bruteforce all ASCII character in increasing lenght sequence.

In the end the flag is:
```
flag{^}
```

P.S. It is important to notice that whenever we reash an hash we must use it's uppercase form.
