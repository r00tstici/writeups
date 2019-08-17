In this web challenge with the following description:
```
This is an easy cipher? I heard it's broken.
```
we were given a minified web page with a script section(look at index.html for the full page):

So the first thing to do is to beautify the code with some online tool and deobfuscate it, then we can look at the functions. We don't need to understand all the functions because at the end of the script we have the important section:

```javascript
if (calcMD5(prompt("What is the password")) === "aa42b234cb05915716c1434058fe1aee16c14340cb059157aa42b234") {
  alert("submit as redpwnctf{PASSWORD}");
} else {
  alert(":(");
}
```

So it seems to be a basic MD5 reverse challenge, in fact if we search for "aa42b234cb05915716c1434058fe1aee16c14340cb059157aa42b234" in a MD5 rainbow table we will find:

```
shazam
```

In the end the flag is:
```
flag{shazam}
```
