#!bin/bash
sudo chmod -R 777 sample.csv
pgbench -c 10 -j 2 -t 50 -f pgturboscript2a.sql provider_lookup | grep 'including' | grep -Eo '[0-9]*\.[0-9]*'  >> sample.csv
brew services restart postgresql
