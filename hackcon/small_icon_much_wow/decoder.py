#!/usr/bin/python

from pyzbar.pyzbar import decode
from PIL import Image
import sys

print(decode(Image.open(sys.argv[1]))[0].data.decode('utf8'))