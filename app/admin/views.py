# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from . import admin
from .. import db

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)
  
@admin.route('/deleteUser')     
def deleteUser():
    print('deleting dat user!')
        
@admin.route('/dashboard', methods=['GET', 'POST'])
def index():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! dashboard !')
    
    
   
    # load login template
    return render_template('admin/admin_dashboard.html')