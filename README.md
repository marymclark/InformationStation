Information Station
===================

Git repository for the College of Education Information Station. This is an application designed for submission and management of student forms for the program.

Installation and Running the Server
-----------------------------------

Before building the project, please be sure to update your system to ensure compatibility. Upon 
loading up your Cloud9 Workspace, please enter the following commands into your command line:

	git clone https://github.com/rhodochrosiite/InformationStation.git
	cd InformationStation
	. setupTest.sh

`setupTest.sh` will install all dependencies and set up your MySQL database. If you would like to 
encapsulate the project's dependencies and run the project with the correct versions, create and 
activate a [Python virtual environment](https://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/).

When you are ready to run the server, please execute the following in your command line:
	
	. runServer.sh 

Common Errors
-------------

A common issue in Cloud9 is that `python.h`, the Python header file, will not be found. To fix this problem,
run:

	sudo apt-get update; sudo apt-get install python-dev -y
	
If your environment does not recognize the `FLASK_APP` path (run.py) please run `python run.py`. If this gives
an error, fix it and the app should be able to run. If an error is not returned, there may be an issue with
bad `import`s in the application.