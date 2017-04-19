sudo service mysql start
export FLASK_CONFIG=development
export FLASK_APP=run.py

rm -rf migrations

echo "drop database if exists coeas" | mysql -u root
echo "create database coeas" | mysql -u root

flask db init
flask db migrate
flask db upgrade

###The following 2 commands add an admin account, and the 3 form's default expired dates

#Create test user
echo "from app import db; from app.models import User; user = User(email='acarlyle@mail.umw.edu', password='123',first_name='Alec',last_name='Carlyle',confirmed=True); db.session.add(user); db.session.commit()" | flask shell
echo "from app import db; from app.models import User; user = User(email='testuser@mail.umw.edu', password='123',first_name='Test',last_name='User',confirmed=True); db.session.add(user); db.session.commit()" | flask shell
#Create admin account
echo "from app import db; from app.models import User; admin = User(email='coe@as.com', password='123',is_admin=True,confirmed=True); db.session.add(admin); db.session.commit()" | flask shell
#Create and fill application deadline table
echo "from app import db; from app.models import ApplicationInformation; form1 = ApplicationInformation(name='post-bac', deadlineDate='2018-04-16'); form2 = ApplicationInformation(name='FifthYear', deadlineDate='2018-04-16'); form3 = ApplicationInformation(name='Undergrad', deadlineDate='2018-04-16'); db.session.add(form1); db.session.add(form2); db.session.add(form3); db.session.commit()" | flask shell