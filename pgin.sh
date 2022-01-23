#! bin/bash
pgbench -i provider_lookup
if ![test -f "sample.csv"]; then
sudo touch sample.csv
fi

