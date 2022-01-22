#!bin/bash
brew services restart postgresql
sudo chmod -R 777 sample.txt
pgbench -c 10 -j 2 -t 50 -f pgturboscript2a.sql provider_lookup >> sample.txt
