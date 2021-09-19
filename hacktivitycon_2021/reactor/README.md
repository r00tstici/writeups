# Reactor - hacktivitycon 2021

- Category: Mobile - Reversing
- Points: 383
- Solves: 103
- Solved by: drw0if

## Description

We built this app to protect the reactor codes

## Solution
We are provided with an `android apk` file, installing it on an emulator we are provided with the following screen:

![main_screen](images/apk_screen.png)

If we provide a pin we can see a string popping out:

![decoded_screen](images/decoded.png)

This string seems not to be the flag, tho.

Since it is an android application we can unpack it with apktool:
```bash
apktool d reactor.apk
```

Opening the apk file with `jadx-gui` and looking inside the `com.reactor.MainActivity` we can notice that the MainActivity extends the `ReactActivity` class: we are dealing with a `react native` application. Those applications aren't compiled to native language so we can find the js code somewhere: in fact digging inside the asset folder we can spot a file called `index.android.bundle` full of js code!

This is a huge block with more than 30k lines so we can't read it all. Searching for the string `Insert the pin` we can identify our component code:
```javascript
__d(function(g, r, i, a, m, e, d) {
    Object.defineProperty(e, "__esModule", {
        value: !0
    }), e.default = void 0;

    var t = r(d[0])(r(d[1])),
        n = (function(t, n) {
            if (!n && t && t.__esModule) return t;
            if (null === t || "object" != typeof t && "function" != typeof t) return {
                default: t
            };
            var l = u(n);
            if (l && l.has(t)) return l.get(t);
            var o = {},
                f = Object.defineProperty && Object.getOwnPropertyDescriptor;
            for (var c in t)
                if ("default" !== c && Object.prototype.hasOwnProperty.call(t, c)) {
                    var p = f ? Object.getOwnPropertyDescriptor(t, c) : null;
                    p && (p.get || p.set) ? Object.defineProperty(o, c, p) : o[c] = t[c]
                } o.default = t, l && l.set(t, o);
            return o
        })(r(d[2])),
        l = r(d[3]);

    function u(t) {
        if ("function" != typeof WeakMap) return null;
        var n = new WeakMap,
            l = new WeakMap;
        return (u = function(t) {
            return t ? l : n
        })(t)
    }

    var o = function() {
        var u = (0, n.useState)(''),
            o = (0, t.default)(u, 2),
            f = o[0],
            c = o[1],
            p = (0, n.useState)(''),
            s = (0, t.default)(p, 2),
            y = s[0],
            v = s[1];
        return n.default.createElement(l.ScrollView, null, n.default.createElement(l.Text, {
            style: {
                fontSize: 45,
                marginTop: 30,
                textAlign: "center"
            }
        }, "\u2622\ufe0f Reactor \u2622\ufe0f"), n.default.createElement(l.Text, {
            style: {
                padding: 10,
                fontSize: 18,
                textAlign: "center"
            }
        }, "Insert the pin to show the reactor codes."), n.default.createElement(l.TextInput, {
            style: {
                height: 40,
                fontSize: 15,
                textAlign: "center"
            },
            placeholder: "PIN",
            keyboardType: "number-pad",
            maxLength: 4,
            onChangeText: function(t) {
                return v(t)
            },
            onSubmitEditing: function(t) {
                c((0, r(d[4]).decrypt)(t.nativeEvent.text)), v("")
            },
            defaultValue: y
        }), n.default.createElement(l.Text, {
            style: {
                padding: 10,
                fontSize: 18,
                textAlign: "center"
            }
        }, f))
    };
    e.default = o
}, 399, [3, 23, 125, 1, 400]);
```

We can notice that the component has an event handler for the `onSubmitEditing` event, this callback uses the method `decrypt` on the textbox content!

Searching for something called `decrypt` we can find:
```javascript
__d(function(g, r, _i, a, m, e, d) {
    var t = r(d[0])(r(d[1])),
        n = "U1VTUE5aVFVXDVEBUFoHDlZcAQYDXApTAg8GA1RaBlQCCVMGB0Q=";

    function o(t, n) {
        for (var o = '', c = t; c.length < n.length;) c += c;
        for (var f = 0; f < n.length; ++f) o += String.fromCharCode(c.charCodeAt(f) ^ n.charCodeAt(f));
        return o
    }
    m.exports.encrypt = function(n, c) {
        return t.default.encode(o(n, c))
    }, m.exports.decrypt = function(c) {
        return o(c, t.default.decode(n))
    }
}, 400, [3, 401]);
```

Once again the `decrypt function` calls a `decode` method, that can be spotted here:

```javascript
__d(function(g, r, _i, a, m, e, d) {
    Object.defineProperty(e, "__esModule", {
        value: !0
    }), e.default = void 0;
    var t = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',
        n = {
            encode: function(n) {
                var c, h, i, o, A, f = [],
                    u = "",
                    l = "",
                    s = 0;
                do {
                    i = (c = n.charCodeAt(s++)) >> 2, o = (3 & c) << 4 | (h = n.charCodeAt(s++)) >> 4, A = (15 & h) << 2 | (u = n.charCodeAt(s++)) >> 6, l = 63 & u, isNaN(h) ? A = l = 64 : isNaN(u) && (l = 64), f.push(t.charAt(i) + t.charAt(o) + t.charAt(A) + t.charAt(l)), c = h = u = "", i = o = A = l = ""
                } while (s < n.length);
                return f.join('')
            },
            encodeFromByteArray: function(n) {
                var c, h, i, o, A, f = [],
                    u = "",
                    l = "",
                    s = 0;
                do {
                    i = (c = n[s++]) >> 2, o = (3 & c) << 4 | (h = n[s++]) >> 4, A = (15 & h) << 2 | (u = n[s++]) >> 6, l = 63 & u, isNaN(h) ? A = l = 64 : isNaN(u) && (l = 64), f.push(t.charAt(i) + t.charAt(o) + t.charAt(A) + t.charAt(l)), c = h = u = "", i = o = A = l = ""
                } while (s < n.length);
                return f.join('')
            },
            decode: function(n) {
                var c, h, i, o, A = "",
                    f = "",
                    u = "",
                    l = 0;
                if (/[^A-Za-z0-9\+\/\=]/g.exec(n)) throw new Error("There were invalid base64 characters in the input text.\nValid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\nExpect errors in decoding.");
                n = n.replace(/[^A-Za-z0-9\+\/\=]/g, "");
                do {
                    c = t.indexOf(n.charAt(l++)) << 2 | (i = t.indexOf(n.charAt(l++))) >> 4, h = (15 & i) << 4 | (o = t.indexOf(n.charAt(l++))) >> 2, f = (3 & o) << 6 | (u = t.indexOf(n.charAt(l++))), A += String.fromCharCode(c), 64 != o && (A += String.fromCharCode(h)), 64 != u && (A += String.fromCharCode(f)), c = h = f = "", i = o = u = ""
                } while (l < n.length);
                return A
            }
        };
    e.default = n
}, 401, []);
```

Putting everything togheter and changing some variable names the relevant code is:
```javascript
var n = "U1VTUE5aVFVXDVEBUFoHDlZcAQYDXApTAg8GA1RaBlQCCVMGB0Q=";
var t = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

function decode(n) {
    var c, h, i, o, A = "",
        f = "",
        u = "",
        l = 0;
    if (/[^A-Za-z0-9\+\/\=]/g.exec(n)) throw new Error("There were invalid base64 characters in the input text.\nValid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\nExpect errors in decoding.");
    n = n.replace(/[^A-Za-z0-9\+\/\=]/g, "");
    do {
        c = t.indexOf(n.charAt(l++)) << 2 | (i = t.indexOf(n.charAt(l++))) >> 4, h = (15 & i) << 4 | (o = t.indexOf(n.charAt(l++))) >> 2, f = (3 & o) << 6 | (u = t.indexOf(n.charAt(l++))), A += String.fromCharCode(c), 64 != o && (A += String.fromCharCode(h)), 64 != u && (A += String.fromCharCode(f)), c = h = f = "", i = o = u = ""
    } while (l < n.length);
    return A
}

function o(key, n) {
    for (var o = '', c = key; c.length < n.length;) c += c;
    for (var f = 0; f < n.length; ++f) o += String.fromCharCode(c.charCodeAt(f) ^ n.charCodeAt(f));
    return o
}

function decrypt(key) {
    return o(key, decode(n))
}
```

A PIN code is usually compose by 4 digits, so we brute-force it with:
```javascript
for(i = 0; i < 10; i++){
    for(j = 0; j < 10; j++){
        for(k = 0; k < 10; k++){
            for(l = 0; l < 10; l++){
                var key = "" + i + j + k + l;
                a = decrypt(key);
                if(a.includes("flag"))
                    console.log(key + " " + a)
            }
        }
    }
}
```

and we got the flag!

```
flag{cfbb4c6ec59ce316e8d7644ac4c70a12}
```
