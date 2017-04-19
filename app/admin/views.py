# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required

from datatables import ColumnDT, DataTables

from . import admin
from .. import db
from ..models import User, ApplicationInformation, Forms, UserForms



def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

        
  
@admin.route('/deleteUser', methods=['POST'])     
def deleteUser():
    print('deleting dat user!')
    
    if request.method == 'POST':
        try:
            data = request.get_json() # Get POSTed JSON from Javascript
        except:
            return jsonify({'Failure':'No request data.'})
            
        print('data: ', data)
        
        #ai = ApplicationInformation.query.filter_by(name=data['button']).first()
        #ai.deadlineDate = data['date']
        
        print(str(data['1']))
        
        user = db.session.query(User).filter(User.email==str(data['1'])).first()
        db.session.delete(user)
        db.session.commit()

        return jsonify({'Success':'Request was valid.'})
        
        
@admin.route('/delApplication', methods=['POST'])     
def delApplication():
    print('deleting dat application!')
    
    if request.method == 'POST':
        try:
            data = request.get_json() # Get POSTed JSON from Javascript
        except:
            return jsonify({'Failure':'No request data.'})
            
        print('data: ', data)
        
        #ai = ApplicationInformation.query.filter_by(name=data['button']).first()
        #ai.deadlineDate = data['date']
        
        print(str(data['1']))
        
        user = db.session.query(User).filter(User.email==str(data['1'])).first()
        form = db.session.query(Forms).filter(Forms.user_id==user.id).first()
        userformentry = db.session.query(UserForms).filter(form.user_id==UserForms.user_id, user.id==UserForms.form_id).first()
        
        #print(form.name)
        db.session.delete(userformentry)
        db.session.commit()

        return jsonify({'Success':'Request was valid.'})


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
        
@admin.route('/delApplicationTable')
def delApplicationTable():
    """Return server side data."""
    
    print('stoff')
        
    print('creating application table')
    
    # defining columns
    columns = [
        ColumnDT(Forms.name),
        ColumnDT(User.email),
        ColumnDT(User.first_name),
        ColumnDT(User.last_name),
    ]
    
    print('params')
    
    params = request.args.to_dict()
    
    # defining the initial query depending on your purpose
    #query = db.session.query(User.id, User.email, User.first_name, User.last_name, User.lastLoginDate).filter(User.is_admin==False)
    query = db.session.query(Forms.name, User.email, User.first_name, User.last_name).\
        filter(User.id==Forms.user_id)
    print('query: ', query)
    
    params = request.args.to_dict()
    
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())
    
    
@admin.route('/userTable')
def userTable():
    """Return server side data."""
    
    print('stoff')
        
    print('creating user table')
    
    # defining columns
    columns = [
        ColumnDT(User.id),
        ColumnDT(User.email),
        ColumnDT(User.first_name),
        ColumnDT(User.last_name),
        ColumnDT(User.lastLoginDate)
    ]
    
    print('params')
    
    params = request.args.to_dict()
    
    # defining the initial query depending on your purpose
    query = db.session.query(User.id, User.email, User.first_name, User.last_name, User.lastLoginDate).filter(User.is_admin==False)
    print('query: ', query)
    
    params = request.args.to_dict()
    
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    
    print('params: ', params)
    print('cols: ', columns)
    print('rowTable: ', rowTable.output_result())
    
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
    
@admin.route('/users', methods=['GET', 'POST'])
def users():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! users !')
    
   
    # load login template
    return render_template('admin/users.html')
    
    
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