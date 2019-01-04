CERT=./pem_keys/younited_prod_ireland.pem
URL=ubuntu@ec2-34-247-48-6.eu-west-1.compute.amazonaws.com

scp -i $CERT main.py $URL:/home/ubuntu/younited/
# scp -i $CERT create_clubs_from_csv.py $URL:/home/ubuntu/younited/
# scp -i $CERT league.csv $URL:/home/ubuntu/younited/

scp -r -i $CERT alembic $URL:/home/ubuntu/younited/
scp -r -i $CERT api $URL:/home/ubuntu/younited/
scp -r -i $CERT assets $URL:/home/ubuntu/younited/
scp -r -i $CERT db $URL:/home/ubuntu/younited/
scp -r -i $CERT pages $URL:/home/ubuntu/younited/
scp -r -i $CERT utils $URL:/home/ubuntu/younited/
scp -r -i $CERT templates $URL:/home/ubuntu/younited/
