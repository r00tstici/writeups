
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