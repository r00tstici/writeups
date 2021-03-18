# Read - DaVinciCTF

- Category: Reverse
- Points: 50
- Solves: 124
- Solved by: Lu191

## Description

Help me! I can't find the password for this binary!

## Analysis

We start analyzing the file that we need to reverse, it's not stripped so it will be easier to reverse because we have all symbols.
Let's start to analyze it with ghidra, looking at the main function.
```
undefined8 main(int param_1,undefined8 *param_2)

{
  int iVar1;
  undefined8 uVar2;
  
  if (param_1 == 2) {
    iVar1 = transform(param_2[1]);
    if (iVar1 == 0) {
      puts("Nice flag");
    }
    else {
      puts("Nice try");
    }
    uVar2 = 0;
  }
  else {
    printf("Usage: %s <password>\n",*param_2);
    uVar2 = 1;
  }
  return uVar2;
}
```

We see that the only function that we'll need to look at is `transform` that is used to check if the password that in this case is also the flag is correct or not, this will be passed as an argument when we launch the binary.
Now we need to analyze the transform function which takes as input the first argument with which the binary is called.

```
void transform(long param_1)

{
  size_t sVar1;
  uint local_24;
  char *local_20;
  
  local_24 = 0;
  while( true ) {
    sVar1 = strlen("wAPcULZh\x7f\x06x\x04LDd\x06~Z\"YtJNice flag");
    if (sVar1 <= (ulong)(long)(int)local_24) break;
    if ((local_24 & 1) == 0) {
      local_20[(int)local_24] = *(byte *)(param_1 + (int)local_24) ^ 0x13;
    }
    else {
      local_20[(int)local_24] = *(byte *)(param_1 + (int)local_24) ^ 0x37;
    }
    local_24 = local_24 + 1;
  }
  strncmp("wAPcULZh\x7f\x06x\x04LDd\x06~Z\"YtJNice flag",local_20,0x16);
  return;
}
```

This function takes the string that we passed as an argument when we called the binary and perform an xor operation with each character of the string, it use a counter variable `local_24` that is set initally to 0 and gets incremented each iteration of the while loop, it's used as an index of the string that is transformed, if the current value of this counter is even the character at the specific index of the string `(input[local_24])` gets xored with 0x13 otherwise it gets xored with 0x37, the loop ends when the counter is equal to the length of a string that is later compared with the transformed string that is modified in the while loop.

## Solution

At this point we now that we can reverse the XOR operation (z = x XOR y then x = z XOR y), but first we need to get the hex values of the string that is used for the last comparison. 

```
                             PASSWD   XREF[3]:     Entry Point(*),                                                             transform:00101221(*), 
                                                   transform:0010123e(*)  
        00102010 77              ??         77h    w
        00102011 41              ??         41h    A
        00102012 50              ??         50h    P
        00102013 63              ??         63h    c
        00102014 55              ??         55h    U
        00102015 4c              ??         4Ch    L
        00102016 5a              ??         5Ah    Z
        00102017 68              ??         68h    h
        00102018 7f              ??         7Fh    
        00102019 06              ??         06h
        0010201a 78              ??         78h    x
        0010201b 04              ??         04h
        0010201c 4c              ??         4Ch    L
        0010201d 44              ??         44h    D
        0010201e 64              ??         64h    d
        0010201f 06              ??         06h
        00102020 7e 5a 22 59     ddw        59225A7Eh
        00102024 74              ??         74h    t
        00102025 4a              ??         4Ah    J
                             DAT_00102026                                    XREF[1]:     main:00101286(*)  
        00102026 4e              ??         4Eh    N
        00102027 69              ??         69h    i
        00102028 63              ??         63h    c
        00102029 65              ??         65h    e
        0010202a 20              ??         20h     
        0010202b 66              ??         66h    f
        0010202c 6c              ??         6Ch    l
        0010202d 61              ??         61h    a
        0010202e 67              ??         67h    g
        0010202f 00              ??         00h

```

Then we wrote the script that performs the xor operations we found in the transform function on this string, and we got the flag.

## Flag

`dvCTF{I_l1k3_sw1mm1ng}`
