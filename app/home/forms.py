# home/forms.py

from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import DataRequired, Email

class EmailForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])