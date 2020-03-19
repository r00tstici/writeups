# msd
### Category: misc
### Description:
You thought Angstrom would have a stereotypical LSB challenge... You were wrong! To spice it up, we're now using the [Most Significant Digit](public.py). Can you still power through it?

Here's the [encoded image](output.png), and here's the [original image](breathe.jpg), for the... well, you'll see.

### Author: JoshDaBosh
### Solution:
In MSD we get two images, one has been encoded with this code

```py
from PIL import Image

im = Image.open('breathe.jpg')
im2 = Image.open("breathe.jpg")

width, height = im.size

flag = "REDACT"
flag = ''.join([str(ord(i)) for i in flag])


def encode(i, d):
    i = list(str(i))
    i[0] = d

    return int(''.join(i))
    

c = 0

for j in range(height):
    for i in range(width):
        data = []
        for a in im.getpixel((i,j)):
            data.append(encode(a, flag[c % len(flag)]))

            c+=1

        im.putpixel((i,j), tuple(data))
        
im.save("output.png")
pixels = im.load()
```

This essentially builds a long numeric string ```flag``` concatenating the byte-values of the characters in the real flag. Then each channel of each pixel is encoded by replacing its most significant digit with one digit from ```flag```.<br>
We can thus reconstruct ```flag``` by taking the MSD of every pixel in the encoded image, and appending it to a string. Or maybe not. Doing this will result in junk output, as we haven't handled the case when zeroes happen to replace the MSD; obviously we can't know whether this is the case without knowing what the value looked like before the encoding (Example: value 61 can be had both by replacing the MSD in 91 with a six and by replacing the MSD in 161 with a zero). We deal with this by comparing the magnitude of the original picture and the encoded one:

```py
decimal = []

for j in range(height):
    for i in range(width):
        for imp, outp in zip(im.getpixel((i,j)), out.getpixel((i,j))):
            imp = str(imp)
            outp = str(outp)
            if len(imp) != len(outp):   #if lengths are different, it means that the MSD 
                decimal += '0'          #of a 3-digit value has been replaced by a zero
            else:
                decimal += outp[0]

decimal = ''.join(decimal)
```

Now we have ```decimal```, the exact reconstruction of the expanded ```flag``` string. We just have to get out of this printable characters, so we can retrieve our flags.<br>
We know ascii printable values range from 32 to 126, so we can't just split the string in 2-digit long pieces and convert it; we have to understand when we have to take a 3 digit long string, and when we have to take a 2 digit long one. The simplest way is checking if it begins with a ```1```. Knowing we can't go under 32, it doesn't make sense to take a 2 digit string if it begins with a one. This is nice, because neither taking a 3 digit string makes sense *if it starts with anything else than a one*.

```py
flag = []

i = 0
while True:
    if decimal[i] == '1':
        flag += chr(int(decimal[i:i+3]))
        i += 3
    else:
        flag += chr(int(decimal[i:i+2]))
        i += 2
    if i == len(decimal):
        break
```

This would make sense, but returns gibberish anyway. So what's wrong?<br>
If ```flag``` was a plain flag, there would be no such problems, but it is actually something else. Doing the conversion by hand shows that the first letters are ```L, o, r, e, m```. So a lorem ipsum, and our flag is hidden in there. Of course there are line feeds too, which carry an ascii value of 12. This is bad. This means that we can't just treat every single string that begins with ```1``` as if it was part of a 3 digit value.<br><br>

We changed our code so that it always tries to use strings that begin with ```1``` in stacks of three, but will trigger a line feed if the next stack can't be completed (if it begins with a ```2```, as no ascii printable characters exist over 126 and between 20 and 29)

```py
i = 0
while True:
    if decimal[i] == '1':
        if decimal[i+1] == '0' and decimal[i+3] == '2':
                flag += '\n'
                i += 2
        else:
            flag += chr(int(decimal[i:i+3]))
            i += 3
    else:
        flag += chr(int(decimal[i:i+2]))
        i += 2
    if i == len(decimal):
        break
```
This might not be perfect, but it was enough to retrieve the complete flag.<br><br>

Here's the complete script:
```py
from PIL import Image
import re

im = Image.open('breathe.jpg')
out = Image.open('output.png')

width, height = out.size

#flag = "REDACT"
#flag = ''.join([str(ord(i)) for i in flag])

decimal = []

for j in range(height):
    for i in range(width):
        for imp, outp in zip(im.getpixel((i,j)), out.getpixel((i,j))):
            imp = str(imp)
            outp = str(outp)
            if len(imp) != len(outp):
                decimal += '0'
            else:
                decimal += outp[0]

decimal = ''.join(decimal)
flag = []

i = 0
while True:
    if decimal[i] == '1':
        if decimal[i+1] == '0' and decimal[i+3] == '2':
                flag += '\n'
                i += 2
        else:
            flag += chr(int(decimal[i:i+3]))
            i += 3
    else:
        flag += chr(int(decimal[i:i+2]))
        i += 2
    if i == len(decimal):
        break

flag = ''.join(flag)
for x in re.findall('actf{.*}', flag):
    print(x)
```

### Flag:
```
actf{inhale_exhale_ezpz-12309biggyhaby}
```