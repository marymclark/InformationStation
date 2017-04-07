# app/home/views.py

from flask import render_template
from flask_login import login_required

from . import home

# Index
@home.route('/')
def index():
    
    return render_template("home/index.html")
    
# User Dashboard
@home.route('/dashboard')
@login_required
def dashboard():
    
    return render_template("home/userdash.html")