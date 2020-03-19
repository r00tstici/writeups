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