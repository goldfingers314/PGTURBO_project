#!bin/bash
sudo chmod -R 777 sample.csv
touch temp.csv
pgbench -c 1 t -1 -f pgturboscript2a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*'   >> sample.csv 
pgbench -c 1 t -1 -f pgturboscript2a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*'   >> sample.csv  
pgbench -c 1 t -1 -f pgturboscript2a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*'   >> sample.csv 
pgbench -c 1 t -1 -f pgturboscript2a.sql provider_lookup | grep 'tps' | grep -Eo '[0-9]*\.[0-9]*'   >> sample.csv 
pg_isready
a=$?
while [ $a -ne 0 ]
do
brew services restart postgresql &
pg_isready 
a=$?
done
