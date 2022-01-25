#! bin/bash
while[$(pg_isready)-ne '0'];do
sudo service postgresql restart
done

