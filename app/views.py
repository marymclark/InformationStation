# Views to display all forms

from flask import render_template, jsonify
from app import app
import helpers

# Data for Javascript

# Send endorsement data to Javascript
@app.route('/api/endorsements')
def getEndorsements():
    return jsonify(helpers.getEndorsements())

# Send school data to Javascript
@app.route('/api/schools')
def getSchools():
    return jsonify(helpers.getSchools())

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
@app.route('/forms/continuation', methods=["GET"])
def continuationForm():
    # Reason for not continuing
    reasons = ['Financial','Grades','Study Abroad','Moving out of Area','Personal','No longer interested in teaching','Other']
    return render_template("forms/continuation.html",years=helpers.nextnYears(5),reasons=reasons)

# Internship Form
@app.route('/forms/internship')
def internshipForm():
    return render_template("forms/internship.html")

# Admission Form
@app.route('/forms/admission')
def admissionForm():
    return render_template("forms/admission.html")