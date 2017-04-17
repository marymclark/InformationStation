# home/forms.py

from flask_wtf import Form
from wtforms import StringField, PasswordField, TextField, SubmitField
from wtforms.validators import DataRequired, Email

class EmailForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset')

class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])