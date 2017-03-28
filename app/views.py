# Direct to all the forms

from flask import render_template
from app import app
from json import load

# Global variables

endorsements = [] 

# Helper functions

def getEndorsements():
    global endorsements
    if not endorsements: # If the endorsements list is empty
        with open('app/data/endorsements.json') as file:
            data = load(file)["data"]
        endorsements = data
    return endorsements

# Routing

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/forms/continuation')
def continuationForm():
    endorsements = getEndorsements()
    return render_template("forms/continuation.html", data={"endorsements":endorsements})

@app.route('/forms/internship')
def internshipForm():
    endorsements = getEndorsements()
    return render_template("forms/internship.html", data={"endorsements":endorsements})

@app.route('/forms/admission')
def admissionForm():
    endorsements = getEndorsements()
    return render_template("forms/admission.html", data={"endorsements":endorsements})