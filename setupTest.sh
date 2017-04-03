#!/bin/sh
sudo pip install -r requirements.txt

sudo service mysql start
echo "drop database if exists coeas" | mysql -u root 
echo "create database coeas" | mysql -u root 
mysql -u root coeas < coeas_mysql.sql

echo 'All done!'
echo 'Now run runServer.sh'

#export FLASK_APP=run.py
#flask run --host '0.0.0.0' --port '8080'
