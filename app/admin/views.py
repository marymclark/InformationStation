# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required

from datatables import ColumnDT, DataTables


from . import admin
from .. import db
from ..models import User, ApplicationInformation



def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

        
  
@admin.route('/deleteUser')     
def deleteUser():
    print('deleting dat user!')
    
@admin.route('/userTable')
def simple_example():
    """Return server side data."""
    
    print('stoff')
        
    print('creating user table')
    
    # defining columns
    columns = [
        ColumnDT(User.id),
        ColumnDT(User.email),
    ]
    
    params = request.args.to_dict()
    
    # defining the initial query depending on your purpose
    query = db.session.query(User)
    
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())
        
@admin.route('/dashboard', methods=['GET', 'POST'])
def index():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! dashboard !')


    query = db.session.query(ApplicationInformation)
    print('querY:', query)
    
    ai = ApplicationInformation.query.all()

    deadlines = []

    for a in ai:
        print a.name, a.deadlineDate
        deadlines.append(a.deadlineDate)
    
   
    # load login template
    return render_template('admin/admin_dashboard.html', fifthyeardeadline=deadlines[0], undergraddeadline=deadlines[1], postbacdeadline=deadlines[2])