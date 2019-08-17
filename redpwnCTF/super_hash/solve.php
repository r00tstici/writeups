<?php
$end = "CD04302CBBD2E0EB259F53FAC7C57EE2";

for ($a = 0; $a < 256; $a++){
    $value = chr($a);
    $hashed =  strtoupper(md5(
        strtoupper(md5(
            strtoupper(md5(
                strtoupper(md5(
                    strtoupper(md5(
                        strtoupper(md5(
                            strtoupper(md5(
                                strtoupper(md5(
                                    strtoupper(md5(
                                        strtoupper(md5($value))
                                    ))
                                ))
                            ))
                        ))
                    ))
                ))
            ))
        ))
    ));

    if ($end === $hashed){
        print "FOUND : " . $value . "\n";
    }
}
?>
