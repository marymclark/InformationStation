# app/home/views.py

from flask import abort, render_template
from flask_login import current_user, login_required

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
    
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")