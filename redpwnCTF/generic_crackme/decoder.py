#!/usr/bin/python

hex = [0x65, 0x70, 0x68, 0x68, 0x7a]
hex = [chr(x-1) for x in hex]

print('flag{' + ''.join(hex) + '}')
