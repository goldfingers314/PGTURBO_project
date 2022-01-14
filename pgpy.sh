#!bin/bash
t="0"
pgbench -i providerlookup
while [ $t -le 100000 ];do
python3 filewriter.py
sudo service postgresql restart
sudo chmod -R 777 sample.txt
pgbench -c 10 -j 2 -t 50 providerlookup >> sample.txt
t=$[$t + 1]
done

