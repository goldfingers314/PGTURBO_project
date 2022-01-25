#! bin/bash
pgbench -i provider_lookup
if [ ! -f "sample.csv" ]; then
sudo touch sample.csv
fi

