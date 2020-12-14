for i in `ls extracted`; do
    gpg --decrypt extracted/$i 2> /dev/null 1>> out/dump
    echo '' >> out/dump
    echo $i
done