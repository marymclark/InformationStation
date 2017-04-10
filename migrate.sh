sudo service mysql start
export FLASK_CONFIG=development
export FLASK_APP=run.py

rm -rf migrations

echo "drop database if exists coeas" | mysql -u root
echo "create database coeas" | mysql -u root

flask db init
flask db migrate
flask db upgrade
