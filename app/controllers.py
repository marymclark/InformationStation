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
    

# TODO this should check that the user is logged in.
@app.route('/forms/continuation', methods=["POST"])
def newContinuationForm():
    try:
        data = request.get_json() # Get POSTed JSON from Javascript
    except:
        return jsonify({'Failure':'No request data.'})
    print(data)
    
    # Check endorsement area
    for endorsement in data['endorsementArea']:
        endorsementArea = helpers.getEndorsementArea(endorsement)
        if (endorsementArea == 0):
            return jsonify({'Failure':'An endorsement area is invalid.'})
        else: print(endorsementArea)
            
    # Check the test requirements have valid tests and dates
    for item in data['testRequirements']:
        # TODO check date
        date = item['date']
        if not (item['exam'] in ['Praxis','VCLA','RVE']):
            return jsonify({'Failure':'A test requirement entry is invalid.'})
            
    # Check graduation
    checkGrad = data['graduation'].split()
    if not ((checkGrad[0] in ['May','August','December']) and (checkGrad[1] in helpers.nextnYears(5))):
        jsonify({'Failure':'Invalid graduation month/year'})
        
    # Add data to database
    # TODO add to database
    
    # For now, return success when valid 
    return jsonify({'Success':'Request was valid.'})