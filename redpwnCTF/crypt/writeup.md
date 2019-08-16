In this web challenge with the following description:
```
Store your most valuable secrets with this new encryption algorithm.
```
we were given a web page with a huge script section and the following output (look at index.html for the full page):
```
your safely encrypted flag is vdDby72W15O2qrnJtqep0cSnsd3HqZzbx7io27C7tZi7lanYx6jPyb2nsczHuMec
```

So the first thing to do is reading the javascript section and understand what it does, we have got an eval statement in which is passed a long expression made up with weird brackets syntax. Eval function though wants a string so let's try to evaluate the weird expression and print it to the console. The result is:

```javascript
f=>btoa(
    [...btoa(f)].map(s=>String.fromCharCode(s.charCodeAt(0)+(location.host.charCodeAt(0)%location.host.charCodeAt(3))))
.join(''))

```

Let's reverse the function to build a decoder for this algorithm:

```javascript
decode = f=>atob(
    [...atob(f)].map(s=>String.fromCharCode(s.charCodeAt(0)-(location.host.charCodeAt(0)%location.host.charCodeAt(3))))
.join(''))
```

Run the decoder with the encrypted flag in the console of the web page:
```javascript
decode('vdDby72W15O2qrnJtqep0cSnsd3HqZzbx7io27C7tZi7lanYx6jPyb2nsczHuMec');
"flag{tHe_H1gh3st_quA11ty_antI_d3buG}"
```

It is important to run the code in the same page because it uses some information like the hostname, but also downloading the webpage helps us avoiding the event that triggers the debugger statement