# Views to display all forms

from flask import render_template, jsonify
from app import app
from json import load

# Data API

@app.route('/api/endorsements')
def getEndorsements():
    try:
        with open('app/data/endorsements.json') as file:
            return jsonify(load(file))
    except:
        return jsonify({"error": "Failed to get file"})

@app.route('/api/schools')
def getSchools():
    try:
        with open('app/data/schools.json') as file:
            return jsonify(load(file))
    except:
        return jsonify({"error": "Failed to get file"})

# Routing

# Index
@app.route('/')
def index():
    return render_template("index.html")
    
# Admin Dashboard...?
@app.route('/dashboard')
def dashboard():
    return "This will be the dashboard...later"

# Continuation Form
@app.route('/forms/continuation')
def continuationForm():
    return render_template("forms/continuation.html")

# Internship Form
@app.route('/forms/internship')
def internshipForm():
    return render_template("forms/internship.html")

# Admission Form
@app.route('/forms/admission')
def admissionForm():
    return render_template("forms/admission.html")