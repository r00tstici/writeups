# **bson**
    - info
        - category: misc
        - points: 331
        - solved by: 4cul, 01baf, crypt3d4ta
    - **Problem**
        - This is the last time i'm asking, who the f is bson??
        - Allegato (bson.json)
            - {"task_name":"bson",  "message_pack_data":"82a36b65795ca4666c6167dc003137372f27362f6c3203352f033f6c6c30033e292803343d2a6f0325332903282e35393803316f2f2f1c3b39032c3d3f3721"}
    - **Writeup**
        - Ci viene fornito un file JSON, al cui interno si trovano 2 campi:
**- task_name**, contenente la stringa "bson";
**- message_pack_data**, contenente una stringa esadecimale.
        - Sicuramente la flag sarà racchiusa in qualche modo all'interno del secondo campo.
        - Facendo una veloce ricerca (e sfruttando anche l'indizio lasciato dal nome "message pack data"), si evince che il campo message_pack_data racchiude al suo interno un messaggio formattato in MessagePack - un efficiente formato di serializzazione binaria. Utilizzando uno dei tanti tool di conversione onlne MessagePack-JSON, si riesce ad ottenere:
```{"key" = 92,
 "flag" = [55,55,47,39,54,47,108,50,3,53,47,3,63,108,108,48,3,62,41,40,
           3,52,61,42,111,3,37,51,41,3,40,46,53,57,56,3,49,111,47,47,
           28,59,57,3,44,61,63,55,33]
 }```
        - 
        - Quello che abbiamo è una chiave ed una flag scomposta in numeri decimali. Dal momento che:
- la flag inizia con due lettere identiche, e il campo flag ha i primi due elementi identici;
- il carattere '{' dista da '}' esattamente di 7 posizioni all'interno della codifica ASCII, e anche 39-33=7 (dove 39 e 33 sono le presunte parentesi graffe di apertura e chiusura della flag, essendo posizionate nel 4th e nell'ultimo elemento del campo flag);
c'è di sicuro una corrispondenza con la tabella **ASCII**. Quindi lo scopo è quello di cercare di ottenere la codifica ascii di ciascun elemento della flag in funzione di key e dell'elemento stesso.
Facendo una **XOR decimale** tra la chiave e ciascun elemento dell'array flag, si ottiene quello che si stava cercando: la codifica ASCII del carattere espressa in decimale.
```#!/bin/env/python3

key = 92
flag = [55,55,47,39,54,47,108,50,3,53,47,3,63,108,108,48,3,62,41,40,
        3,52,61,42,111,3,37,51,41,3,40,46,53,57,56,3,49,111,47,47,
        28,59,57,3,44,61,63,55,33]
ascii_flag = []

for item in flag:
    xor_result = key^item
    ascii_flag.append(chr(xor_result))

for item in ascii_flag: print(item, end="")```
        - 
    - flag: kks{js0n_is_c00l_but_hav3_you_tried_m3ss@ge_pack}
