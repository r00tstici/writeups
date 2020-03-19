# ws1
### Category: misc
### Description:
Find my password from this [recording](recording.pcapng) (:
### Author: JoshDaBosh

### Solution:
the flag has been transmitted in clear text so we can strings the file and grep it
```bash
strings recording.pcapng | grep 'actf{.*}'
```
### Flag:
```
actf{wireshark_isn't_so_bad_huh-a9d8g99ikdf}
```