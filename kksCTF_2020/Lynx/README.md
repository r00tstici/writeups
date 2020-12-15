# Lynx

Category: Web

Points: 204

Solved by: hdesk

## Problem

Hello! We're BluePeace organisation, and we introduce the new project - Lynx Forum!

## Writeup

I knew of a command line based browser named lynx, so
```
$ yay -S lynx
$ lynx http://tasks.kksctf.ru:30070/
```

```
                                                    WELCOME

                                 Let's defend our friend - Lynx - from robots!
                                              (C) BluePeace, 2053
```

Says something about robots, so:


```
$ lynx http://tasks.kksctf.ru:30070/robots.txt

  User-agent: * Disallow: /a4d81e99fda29123aee9d4bb
```

```
$ lynx http://tasks.kksctf.ru:30070/a4d81e99fda29123aee9d4bb

  kks{s0m3_CLI_br0ws3rs_4r3_us3ful}
```
