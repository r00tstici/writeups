# Woooosh
### Category: web
### Description:

Clam's tired of people hacking his sites so he spammed obfuscation on his new game. I have a feeling that behind that wall of obfuscated javascript there's still a vulnerable site though. Can you get enough points to get the flag? I also found the [backend source](index.js).


### Author: aplet123

Our js client was heavily obfuscated, so we went directly for traffic analysis, using burpsuite. We found some interesting data

```
Server -> Client:
--------------------------------------
362:42["shapes",[{"x":473,"y":133},{"x":489,"y":70},{"x":67,"y":241},{"x":229,"y":297},{"x":273,"y":12},{"x":386,"y":205},{"x":172,"y":37},{"x":466,"y":135},{"x":98,"y":213},{"x":265,"y":247},{"x":377,"y":3},{"x":359,"y":54},{"x":386,"y":255},{"x":339,"y":289},{"x":244,"y":48},{"x":71,"y":184},{"x":262,"y":96},{"x":286,"y":163},{"x":367,"y":73},{"x":186,"y":240}]]

Client -> Server:
--------------------------------------
1:225:42["click",318,88.015625] (Response: ok)
--------------------------------------
11:42["start"] (Response: ok)
```

It seems that the client will send commands to the server, then get a list of coordinates, necessary to draw the shapes. We want to know how the circle is created, and it isn't mentioned at all in the sent data. Retrieving it through the client is not viable due to obfuscation. But the server source code has something for us

```js
if (dist(game.shapes[0].x, game.shapes[1].y, x, y) < 10) {
                game.score++;
    }
```

This means that the circle is drawn at the x coordinate of the first shape, and the y coordinate of the second one. We now know where to click, but how?
We first tried creating a bot using python-requests, but the only reply from the server we were getting was ```1:1```.<br>
Nevermind, python is too boring anyway.<br>
We first wanted to hijack the client function that sent clicks, to always send correct ones, but obfuscation meant no.
The debugger was also disabled, along with ``` console.log ```, ```console.error```, and pretty much anything else.<br>

Time to learn how socket.io works (not really).<br>
From the docs we got that we could use something like ```socket.emit(data)``` to forge our request, using the command formats we got using burpsuite.
Luckily we had a ```socket``` object already set up and ready to go, so we start the game by doing

```js
socket.emit('start');
```
We could set up a callback for when the client receives ```'shapes'``` events, but we love to live on the edge. So we're going to check for an update in an array, conveniently called ```shapes```. We do this by declaring two global variables, and updating them once we see a difference

```js
x = 0;
y = 0;

while (true) {
    await new Promise(r => setTimeout(r, 100)); //sleeping 100ms to not crash
    let x1, y2;
    try { //this is in a try because the array is not defined from the beginning
        x1 = shapes[0].x; //the indexes are mismatched due to circle being at
        y2 = shapes[1].y; //x0, y1 (see backend code)
    } catch(error) {} //no logging because disabled
```

Once we know we have valid coords

```js
if (x1 != x && y2 != y) {
```
we can sumbit them, by sending a ```'click'``` command

```js
x = x1;
        y = y2;
        socket.emit('click', x, y);
    }

}
```

This will be repeated over and over, as this is in a while (true) cycle
<br><br>
<br>
This is the full code, that has to be pasted in the browser's console:

```js
socket.emit('start');

x = 0;
y = 0;

while (true) {
    await new Promise(r => setTimeout(r, 100));
    let x1, y2;
    try {
        x1 = shapes[0].x;
        y2 = shapes[1].y;
    } catch(error) {}
    if (x1 != x && y2 != y) {
        x = x1;
        y = y2;
        socket.emit('click', x, y);
    }

}
```

### Flag: 
```
actf{w0000sh_1s_th3_s0und_0f_th3_r3qu3st_fly1ng_p4st_th3_fr0nt3nd}
```