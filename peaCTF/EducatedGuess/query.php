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
