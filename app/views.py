# Direct to all the forms

from flask import render_template
from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/forms/continuation')
def continuationForm():
    return render_template("forms/continuation.html")

@app.route('/forms/internship')
def internshipForm():
    return render_template("forms/internship.html")

@app.route('/forms/admission')
def admissionForm():
    return render_template("forms/admission.html")