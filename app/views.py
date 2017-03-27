# Direct to all the forms

from flask import render_template
from app import app

@app.route('/')
def index():
    return "Hello World!"
    #render_template('index.html')

@app.route('/forms/continuation')
def continuationForm():
    render_template("forms/continuation.html")

@app.route('/forms/internship')
def internshipForm():
    render_template("forms/internship.html")

@app.route('/forms/admission')
def admissionForm():
    render_template("forms/admission.html")