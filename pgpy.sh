#!bin/bash
t="0"
pgbench -i providerlookup
sudo touch sample.txt
while [ $t -le 100000 ];do
python3 filewriter.py
sudo service postgresql restart
sudo chmod -R 777 sample.txt
pgbench -c 10 -j 2 -t 50 -f pgturboscript2a.sql providerlookup >> sample.txt
t=$[$t + 1]
done

