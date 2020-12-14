mkdir downloaded
for i in {1..3500};do
    wget http://tasks.kksctf.ru:30030/reports/$i -P downloaded
done
