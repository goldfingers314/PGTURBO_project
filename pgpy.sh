#!bin/bash
sudo service postgresql restart
sudo chmod -R 777 sample.txt
pgbench -c 10 -j 2 -t 50 -f pgturboscript1.sql providerlookup >> sample.txt


