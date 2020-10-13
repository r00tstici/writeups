# LimboZone -?-> LimboZ0ne

Category: coding

Points: 200

Solved by: drw0if, 0xThorn

## Problem

At first, R-Boy discovers the ‘limbo zone’ where, caught in a trap, he meets Virgilia, a guide and protector of the temporal dimension. Virgilia has probably been trapped by Zer0, but R-Boy can release her by decrypting the code.

## Writeup

We are provided with a 7z archive, decompressing it we got 4 files:

- level_0.png
- lev3l_0.png
- ForceLevel.py
- level_1.7z

The .pngs are two `seems equal` pictures, the new archive is password protected and the python script contains:
```python
# ForceLevel.py
def tryOpen(password):
    # TODO
    pass


def main():
    for x in range(0, 10000):
        for y in range(0, 10000):
            for r1 in range (0, 256):
                for g1 in range (0, 256):
                    for b1 in range (0, 256):
                        for r2 in range (0, 256):
                            for g2 in range (0, 256):
                                for b2 in range (0, 256):
                                    xy = str(x) + str(y)
                                    rgb1 = '{:0{}X}'.format(r1, 2) + '{:0{}X}'.format(g1, 2) + '{:0{}X}'.format(b1, 2)
                                    rgb2 = '{:0{}X}'.format(r2, 2) + '{:0{}X}'.format(g2, 2) + '{:0{}X}'.format(b2, 2)
                                    tryOpen(xy + rgb1 + rgb2)


if __name__ == "__main__":
    main()
```

So it is clear enough that in some weird way we must recover the password starting from the two pictures. We wrote a few python lines to loop the two pictures and find the only position whose pixels are different in the two images, we then applied the same composition from the provided script and we got a string, probably the archive password. We firstly tried to open the archive but we got wrong password... We applied the script again inverting che images so that first comes `level_0.png` and then `lev3l_0.png`. We got the right ones so we passed the level.
```
191186E2DBDB1B90CA
```

Next level provided us two more images and another 7z archive, we applied the same logic and we got another password. We started automatizing out script so that it can achive that task alone. At some point our script started failing, we opened the images and without surprise images started to be transformed, mirrored around Y axis, X axis and so on. We implemented more algorithm and restarted the process from that point.

In the end we implemented:

- mirror Y
- mirror X
- mirror X and Y
- rotate clockwise by 90°
- rotate counter clockwise by 90°
- rotate counter clockwise by 90° and mirror Y
- rotate counter clockwise by 90° and mirror X

The policy we applied to decide wich transformation to apply is that we try the mirror only if the two images have the same size and we apply rotations otherwise. Then we attempt to find the different pixel and print the password only if there is only one different pixel, otherwise we discard that transformation and attempt another one.

So we chained a shell script to extract archive, cleanup the old ones (for memory reason) and call the python algorithm to process images.

After `1024` iterations we got `level_1024.txt` file with the flag.

### Flag:
```
{FLG:p1xel0ut0fBound3xcept1on_tr4p_1s_shutt1ng_d0wn}
```

`brute.py`
```python
import sys
from PIL import Image

if len(sys.argv) < 3:
    print(f'{sys.argv[0]} file.png fil3.png')
    exit()


def makePassword(x, y, r1, g1, b1, r2, g2, b2):
    xy = str(x) + str(y)
    rgb1 = '{:0{}X}'.format(r1, 2) + '{:0{}X}'.format(g1, 2) + '{:0{}X}'.format(b1, 2)
    rgb2 = '{:0{}X}'.format(r2, 2) + '{:0{}X}'.format(g2, 2) + '{:0{}X}'.format(b2, 2)

    return xy + rgb1 + rgb2


img1 = Image.open(sys.argv[1])
img2 = Image.open(sys.argv[2])

width, heigth = img1.size


def findPassword(algorithm):
    passwords = []
    for x in range(width):
        for y in range(heigth):
            rgb1 = img1.getpixel((x, y))
            try:
                rgb2 = img2.getpixel(algorithm(x, y))
            except:
                return None

            if rgb1 != rgb2:
                password = makePassword(x, y, *rgb1, *rgb2)
                passwords.append(password)

        if len(passwords) > 1:
            return None

    return passwords[0]


transformations = []

normal = lambda x,y: (x,y)

# Rotate around x axis
rotateX = lambda x, y: (x, heigth - y - 1)
# Rotate around y axis
rotateY = lambda x, y: (width - x - 1, y)
# Rotate around x and y axis
rotateXY = lambda x,y: (width - x - 1, heigth - y - 1)

# Rotate clockwise 90°
rotateC90 = lambda x,y: (heigth - y - 1, x)
# Rotate counterclockwise 90°
rotateCC90 = lambda x,y: (y, width - x - 1)

# Rotate counterclockwise 90° AND Mirror around X axis
rotateCC90MirrorY = lambda x,y: (heigth - y - 1, width - x - 1)
# Rotate counterclockwise 90° AND Mirror around X axis
rotateCC90MirrorX = lambda x,y: (y, width - (width-x-1) - 1)

# Mirroring
if img1.size == img2.size:
    transformations += [
        normal,
        rotateX,
        rotateY,
        rotateXY,
    ]

# Rotating and more
if img1.size[0] == img2.size[1]:
    transformations += [
        rotateC90,
        rotateCC90,
        rotateCC90MirrorY,
        rotateCC90MirrorX
    ]

for l in transformations:
    pwd = findPassword(l)

    if pwd:
        print(pwd)
        exit(0)

exit(12)
```


`automatize.sh`
```bash
#/bin/sh

i=0

while true; do
    password=$(python3 brute.py "level_$i.png" "lev3l_$i.png")

    if [ $? -eq 12 ]
    then
        echo "Implement new algorithm"
        exit 1
    fi

    i=$(($i+1))

    echo "$i -> $password"

    7z x "level_$i.7z" -p$password > /dev/null

    if [ $? -eq 0 ]
    then
        rm "level_$i.7z"
    else
        echo "Failure" >&2
        exit 1
    fi

done
```
