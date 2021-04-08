# Revex - angstromCTF 2021

- Category: Reverse
- Points: 75
- Solves: 178
- Solved by: drw0if

## Description

As an active reddit user, clam frequently browses r/ProgrammerHumor. However, the reposts about how hard regex is makes him go >:((((. So, clam decided to show them who's boss.

`^(?=.*re)(?=.{21}[^_]{4}\}$)(?=.{14}b[^_]{2})(?=.{8}[C-L])(?=.{8}[B-F])(?=.{8}[^B-DF])(?=.{7}G(?<pepega>..).{7}t\k<pepega>)(?=.*u[^z].$)(?=.{11}(?<pepeega>[13])s.{2}(?!\k<pepeega>)[13]s)(?=.*_.{2}_)(?=actf\{)(?=.{21}[p-t])(?=.*1.*3)(?=.{20}(?=.*u)(?=.*y)(?=.*z)(?=.*q)(?=.*_))(?=.*Ex)`

## Solution
I analyzed the regex block by block and built up the string:

`(?=.*re)` 		                        => "re" in flag

`(?=.{21}[^_]{4}\}$)` 	                => 25 characters, the last 4 are not "_" and in the end "}"

`(?=.{14}b[^_]{2})`	                    => character 15 is "b" and the next 2 characters are not "_"

`(?=.{8}[C-L])`		                    => character 9 is in range [C-L]

`(?=.{8}[B-F])`		                    => character 9 is in range [B-F] => [B-F] and [C-L] = [CDEF]

`(?=.{8}[^B-DF])`		                    => character 9 is not [B-DF] => character 9 is E

`(?=.{7}G(?<pepega>..).{7}t\k<pepega>)`   => character 8 is G, 18 is t and characters 9-10 are equals to 19-20

`(?=.*u[^z].$)`                           => character 23 is "u" and character 24 is not "z"

`(?=.{11}(?<pepeega>[13])s.{2}(?!\k<pepeega>)[13]s)`
    => characters 13 and 18 is "s", character 12 is [13] and character character 17 is the opposite of 12

`(?=actf\{)`                              => starts with "actf{"

`(?=.{21}[p-t])`                          => character 22 is in range [p-t]

`(?=.*_.{2}_)`                            => _??_

`(?=.*1.*3)`                              => there is 1 and then 3

`(?=.*Ex)`                                => contains Ex

`(?=.{20}(?=.*u)(?=.*y)(?=.*z)(?=.*q)(?=.*_))` => Contains u,y,z,q,_ after 20 characters

```
actf{reGEx_1s_b3stEx_qzuy}
```