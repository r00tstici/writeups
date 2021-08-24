import binascii

rm = [b""]*256
rm[4] = b"\x0f"
rm[5] = b"\x05\x06\x05\x05\x06"
rm[6] = b"\x1d\x1d\x1d\x1d\x1d"
rm[7] = b"\x15\x15\x15\x16\x16"
rm[8] = b"\x6e\x6d\x6d\x6e\x6d\x6e"
rm[9] = b"\x66\x66\x66\x66"
rm[10] = b"\x7e\x7d\x7d\x7e"
rm[11] = b"\x75\x76\x76\x75"
rm[12] = b"\x00"
rm[13] = b"\x46\x46\x46\x46"
rm[14] = b"\x5e\x5d\x5d\x5e"
rm[15] = b"\x55\x56\x56\x55"
rm[36] = b"\x0c\x0f\x0c\x0f\x0c\x0c"
rm[37] = b"\x04\x07\x04\x04\x07\x04"
rm[38] = b"\x1f\x1c\x1c\x1c\x1c"
rm[39] = b"\x14\x14\x14\x14\x17"
rm[40] = b"\x6f\x6c"
rm[41] = b"\x67\x67"
rm[42] = b"\x7c\x7c\x7f\x7c"
rm[43] = b"\x74\x77\x74\x74"
rm[44] = b"\x4f\x4c"
rm[45] = b"\x47\x47"
rm[46] = b"\x5c\x5c\x5f\x5c"
rm[47] = b"\x54\x57\x54\x54"
rm[68] = b"\x00"
rm[69] = b"\x00"
rm[70] = b"\x1c\x1c\x1f\x1f\x1f"
rm[71] = b"\x17\x17\x17\x14\x14\x14"
rm[72] = b"\x6f\x6c\x6c\x6c"
rm[73] = b"\x64\x67\x67\x67"
rm[74] = b"\x7c\x7f\x7c"
rm[75] = b"\x77\x77\x74\x74"
rm[76] = b"\x4f\x4c\x4c\x4c"
rm[77] = b"\x44\x47\x47\x47"
rm[78] = b"\x5c\x5f\x5c"
rm[79] = b"\x57\x57\x54\x54"
rm[100] = b"\x00"
rm[101] = b"\x05\x06\x05\x06\x05"
rm[102] = b"\x1d\x1d\x1d\x1e\x1e"
rm[103] = b"\x16\x15\x16\x15\x16\x15"
rm[104] = b"\x6e\x6d\x6e\x6d"
rm[105] = b"\x66\x65\x66"
rm[106] = b"\x7d\x7d\x7d"
rm[107] = b"\x00"
rm[108] = b"\x4e\x4d\x4e\x4d"
rm[109] = b"\x46\x45\x46"
rm[110] = b"\x5d\x5d\x5d"
rm[111] = b"\x00"
rm[132] = b"\x0a\x0a\x0a\x0a\x0a"
rm[133] = b"\x01\x01\x02\x02\x01\x01"
rm[134] = b"\x1a\x1a\x1a\x1a\x19"
rm[135] = b"\x00"
rm[136] = b"\x69\x6a\x6a"
rm[137] = b"\x62\x61\x62\x62"
rm[138] = b"\x79"
rm[139] = b"\x00"
rm[140] = b"\x49\x4a\x4a"
rm[141] = b"\x42\x41\x42\x42"
rm[142] = b"\x59"
rm[143] = b"\x00"
rm[164] = b"\x00"
rm[165] = b"\x00\x03\x03\x03\x03\x00"
rm[166] = b"\x1b\x1b\x1b\x1b\x1b"
rm[167] = b"\x10\x13\x13\x13\x10"
rm[168] = b"\x6b"
rm[169] = b"\x60\x60"
rm[170] = b"\x7b\x7b\x78"
rm[171] = b"\x00"
rm[172] = b"\x4b"
rm[173] = b"\x40\x40"
rm[174] = b"\x5b\x5b\x58"
rm[175] = b"\x00"
rm[196] = b"\x08\x0b\x08\x08\x08"
rm[197] = b"\x00\x03\x00\x03\x00\x03"
rm[198] = b"\x1b\x18\x18\x18\x18"
rm[199] = b"\x00"
rm[200] = b"\x68\x68\x6b\x68"
rm[201] = b"\x63\x60"
rm[202] = b"\x78\x78\x78\x7b"
rm[203] = b"\x00"
rm[204] = b"\x48\x48\x4b\x48"
rm[205] = b"\x43\x40"
rm[206] = b"\x58\x58\x58\x5b"
rm[207] = b"\x00"
rm[228] = b"\x09\x0a\x0a\x0a\x0a\x09"
rm[229] = b"\x02\x01\x01\x02\x01"
rm[230] = b"\x1a\x1a\x19\x19\x19"
rm[231] = b"\x11\x11\x12\x12\x11\x11"
rm[232] = b"\x6a\x6a\x69"
rm[233] = b"\x62\x62\x62"
rm[234] = b"\x79\x7a\x7a"
rm[235] = b"\x71\x71\x72\x72\x71\x72"
rm[236] = b"\x4a\x4a\x49"
rm[237] = b"\x42\x42\x42"
rm[238] = b"\x59\x5a\x5a"
xm = 1056017893861212352

def ror(v, s):
    b = s % 8
    return ((v << b) & 0xFF) | ((v >> (8 - b)) & 0xFF)

def rol(v, s):
    b = s % 8
    return ((v >> b) & 0xFF) | ((v << (8 - b)) & 0xFF)

def encode_fl(c):
    return rol(c, 3)

def encode_fr(c):
    return ror(c, 5)

def encode_fx(c, x):
    return bytearray([y^c for y in x])

def encode_fm(c):
    global rm
    a = rm[encode_fl(c)]
    a = bytearray([encode_fr(x) for x in a])
    a = encode_fx(c, a)
    return a

def decode_fm(a):
    global decode_fm_lkp
    return decode_fm_lkp[bytes(a)]

def encode(plaintext):
    global xm
    text = bytearray()
    text2 = b'/'.join([encode_fm(x) for x in plaintext])

    array = [
        (xm & 255) & 0xFF,
        (xm >> 8 & 255) & 0xFF,
        (xm >> 16 & 255) & 0xFF,
        (xm >> 24 & 255) & 0xFF,
        (xm >> 32 & 255) & 0xFF,
        (xm >> 40 & 255) & 0xFF,
        (xm >> 48 & 255) & 0xFF,
        (xm >> 56 & 255) & 0xFF,
    ]

    for i in range(len(text2)):
        text.append(text2[i] ^ array[i % len(array)])

    return text

def decode(ciphertext):
    global xm
    array = [
        (xm & 255) & 0xFF,
        (xm >> 8 & 255) & 0xFF,
        (xm >> 16 & 255) & 0xFF,
        (xm >> 24 & 255) & 0xFF,
        (xm >> 32 & 255) & 0xFF,
        (xm >> 40 & 255) & 0xFF,
        (xm >> 48 & 255) & 0xFF,
        (xm >> 56 & 255) & 0xFF,
    ]

    text2 = bytearray()
    for i in range(len(ciphertext)):
        text2.append(ciphertext[i] ^ array[i % len(array)])

    text2 = text2.split(b"/")
    plaintext = [chr(decode_fm(x)) for x in text2]
    plaintext = ''.join(plaintext).encode()
    return plaintext

decode_fm_lkp = dict()
for i in range(256):
    decode_fm_lkp[bytes(encode_fm(i))] = i

print(decode(binascii.unhexlify('3c3cf1df89fe832aefcc22fc82017cd57bef01df54235e21414122d78a9d88cfef3cf10c829ee32ae4ef01dfa1951cd51b7b22fc82433ef7ef418cdf8a9d802101ef64f9a495268fef18d52882324f217b1bd64b82017cd57bef01df255288f7593922712c958029e7efccdf081f8808a6efd5287595f821482822f6cb95f821cceff4695495268fefe72ad7821a67ae0060ad')))
