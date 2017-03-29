Information Station
===================

Git repository for the College of Education Information Station. This is an application designed for submission and management of student forms for the program.

Installation
------------

The application's dependencies can be found in the requirements.txt file. These can be installed using `pip install -r requirements.txt`. A virtual environment is recommended for managing these dependencies. After these are installed, set up the basics of Postgres and create the application database using `coeas.sql`:

	sudo service postgresql start
	sudo sudo -u postgres psql
	/password
	#Create your new password here, then quit

	#Log into the postgres account with your new password
	psql -U postgres -h localhost

Lastly, run the Flask application by setting the `FLASK_APP` environment variable to the main file and run the app:

	export FLASK_APP=run.py
	flask run

