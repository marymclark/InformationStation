# Views to display all forms

from flask import render_template, jsonify, request
from app import app
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import helpers
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
#from flask_sqlalchemy import SQLAlchemy
#db = SQLAlchemy(app)


# Data for Javascript

# Send endorsement data to Javascript
@app.route('/api/endorsements')
def getEndorsements():
    return jsonify(helpers.getEndorsements())

# Send school data to Javascript
@app.route('/api/schools')
def getSchools():
    return jsonify(helpers.getSchools())
    
# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = helpers.LoginForm(request.form)
    print form.errors
    if request.method == 'POST':
        if form.validate():
            email=request.form['email']
            password=request.form['password']
            print email
            print password
#            cur = mysql.connection.cursor()
#            cur.execute("""select * from users where email = %s AND password = crypt(%s, password);""", (email, password))
#            results = cur.fetchone()
#            print results
            if ((email == "testingteam@umw.edu" and password == "coeas") or
                (email == "hzontine@umw.edu" and password == "coeas")):
                user = helpers.User(1,email,password)
                login_user(user)
                print "Logged In"
                return render_template("userdash.html", user=email)
            else:
                print "No account associated with that email and password"
        else:
            print "Error-- missing email and/or password"
    return render_template("login.html")

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("index.html")      

    
# Admin Dashboard...?
@app.route('/admindashboard')
def adminDashboard():
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