sudo apt-get install vim tmux -y
sudo apt-get install python3-pip -y
sudo pip3 install flask
sudo pip3 install SQLAlchemy
sudo pip3 install alembic 

sudo apt update -y
sudo apt-get install postgresql postgresql-contrib -y
sudo apt-get install postgresql-server-dev-9.3 -y
sudo pip3 install psycopg2

# Set up the nice colours on the command line
sudo cp /vagrant/.bashrc /home/ubuntu/.bashrc