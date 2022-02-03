# Most Secure Calculator 1 - knightctf

- Category: Web
- Points: 50
- Solves: 338
- Solved by: raff01

## Description

Challenge Link : http://198.211.115.81:9003/

## Solution

The challenge consists of a simple PHP calculator that evaluates math expressions. 

![alt text](./pictures/1.png)


If you try to insert symbols like letters you'll receive a PHP error referred to `eval()` function, perhaps we can inject PHP scripts... let's try with this payload `1-1;echo("hello")`:


![alt text](./pictures/2.png)
<p>...it works!<br>
There's a comment into the web page: </p>

```html
<!-- 
        Hi Selina, 
        I learned about eval today and tomorrow I will learn about regex. I have build a calculator for your child.
        I have hidden some interesting things in flag.txt and I know you can read that file.
    -->
```


so we have to read the file flag.txt... Let's use the PHP `system()` function to execute os commands like `ls` and `cat`:

![alt text](./pictures/3.png)
![alt text](./pictures/4.png)

## Flag
```
KCTF{WaS_mY_cAlCuLaToR_sAfE}
```






