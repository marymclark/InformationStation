# Helper functions for the mvc

import datetime
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, PasswordField

from json import load

class LoginForm(Form):
    email = TextField('UMW Email:', validators=[validators.required()])
    password = TextField('Password:', validators=[validators.required()])

class RegisterForm(Form):
    first = StringField('First Name: ', validators=[validators.DataRequired()])
    last = StringField('Last Name: ', validators=[validators.DataRequired()])
    email = StringField('UMW Email: ', validators=[validators.DataRequired()])
    password1 = StringField('Password: ', validators=[validators.DataRequired()])
    password2 = StringField('Confirm Password: ', validators=[validators.DataRequired()])

# Get the next n years for a form
def nextnYears(n):
    year = datetime.datetime.now().year
    return [year+i for i in range(0,n)]
    
def getEndorsements():
    try:
        with open('app/data/endorsements.json') as file:
            return load(file)
    except:
        return ({"error": "Failed to get file"})
        
def getEndorsementArea(key):
    endorsements = getEndorsements()['data']
    key = [i for i in key if i is not None] # Remove None values; remaining 1-3 values should cooardinate to endorsementarea
    endorsementArea = ''
    try:
        for i in range(0,len(key)):
            endorsementArea += (endorsements[key[i]]['title'])
            if i < len(key)-1:
                endorsementArea += ', '
                endorsements = endorsements[key[i]]['subcategories']
        return endorsementArea 
    except:
        print('Error getting endorsementArea; so far: "'+endorsementArea+'"')
        return 0
        
def getSchools():
    try:
        with open('app/data/schools.json') as file:
            return load(file)
    except:
        return ({"error": "Failed to get file"})