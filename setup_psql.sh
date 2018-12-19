# sudo -i -u postgres
# psql
# CREATE DATABASE younighted_db;
# CREATE ROLE younited_user LOGIN PASSWORD 'S0up3rF00t8aLL';
# GRANT ALL PRIVILEGES ON DATABASE younited_db TO younited_user;

sudo -i -u postgres
psql -c 'CREATE DATABASE younighted_db;'
psql -c "CREATE ROLE younited_user LOGIN PASSWORD 'S0up3rF00t8aLL';"
psql -c 'GRANT ALL PRIVILEGES ON DATABASE younited_db TO younited_user;'
exit

#psql -U younited_user -h 127.0.0.1 younited_db -c "" --password "S0up3rF00t8aLL"

#To log into psql
#psql -U younited_user -h 127.0.0.1 younited_db -W