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


@admin.route('/updateDeadline', methods=['POST'])
def updateDeadline():
    if request.method == 'POST':
        try:
            data = request.get_json() # Get POSTed JSON from Javascript
        except:
            return jsonify({'Failure':'No request data.'})
            
        print('data: ', data)
        
        ai = ApplicationInformation.query.filter_by(name=data['button']).first()
        ai.deadlineDate = data['date']
        
        #db.session.query(ApplicationInformation).filter_by(id=id).update({"date":data['date']})
        
        print(data['date'])
        #print(ai.date)
       # db.session.merge(ai)
        db.session.commit()
        
        if data['button'] == 'post-bac':
            print('yaass')
            

        return jsonify({'Success':'Request was valid.'})
    
    
@admin.route('/data')
def data():
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
    
@admin.route('/database', methods=['GET', 'POST'])
def database():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! database !')
    
   
    # load login template
    return render_template('admin/database.html')
    
@admin.route('/export', methods=['GET', 'POST'])
def export():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! export !')
    
   
    # load login template
    return render_template('admin/export.html')
    
    
@admin.route('/deadlines', methods=['GET', 'POST'])
def deadlines():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! deadlines !')


    query = db.session.query(ApplicationInformation)
    print('querY:', query)
    
    ai = ApplicationInformation.query.all()

    deadlines = []

    for a in ai:
        print a.name, a.deadlineDate
        deadlines.append(a.deadlineDate)
    
   
    # load login template
    return render_template('admin/deadlines.html', fifthyeardeadline=deadlines[1], undergraddeadline=deadlines[2], postbacdeadline=deadlines[0])
        
        
@admin.route('/dashboard', methods=['GET', 'POST'])
def index():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! dashboard !')
    
   
    # load login template
    return render_template('admin/admin_dashboard.html')