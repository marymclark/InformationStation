# Controllers for manipulating models

from flask import request, jsonify, render_template
from app import app
import helpers
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy(app)



# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = helpers.RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            email=request.form['email']
            fname=request.form['first']
            lname=request.form['last']
            password1=request.form['password1']
            password2=request.form['password2']
            print email
            print password1
            print password2
            return render_template("login.html")
        else:
            print form.errors
    return render_template("register.html")