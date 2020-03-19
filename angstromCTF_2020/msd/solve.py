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
