# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for, request, jsonify, send_file, json
from flask_login import current_user, login_required
import csv
import io
import os
from StringIO import StringIO

from datatables import ColumnDT, DataTables

from . import admin
from .. import db
from ..models import User, ApplicationInformation, Forms, UserForms, Form_FifthYear, FifthYearMasters, FifthYearExamsNeeded, Endorsement, PracticumHistory, PracticumGrades



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
        
@admin.route('/exApplication', methods=['POST'])     
def exApplication():
    print('exporting dat app!')
    
    if request.method == 'POST':
        try:
            data = request.get_json() # Get POSTed JSON from Javascript
        except:
            return jsonify({'Failure':'No request data.'})
            
        print('data: ', data)
        
        user = db.session.query(User).filter(User.email==str(data['2'])).first()
        print('user email: ', str(data['2']))
        form = db.session.query(Forms).filter(Forms.user_id==user.id).first()
        
        print('userEmail: ', user.email)
        print('formName: ', form.name)
        userformentry = db.session.query(UserForms).filter(form.user_id==UserForms.user_id, user.id==UserForms.form_id).first()
        
        #Form_FifthYear, FifthYearMasters, FifthYearExamsNeeded, Endorsement, PracticumHistory
        #EXPORT FIFTHYEAR FORM
        if str(data['0'] == 'Form_FifthYear'):
            print(userformentry.user_id, ' ', userformentry.form_id)
            fifthyear = db.session.query(Form_FifthYear).filter(Form_FifthYear.user_id==userformentry.user_id, Form_FifthYear.form_id==userformentry.form_id).first()
            #print(fifthyear.termgraduating)
            fifthyearmasters = db.session.query(FifthYearMasters).filter(FifthYearMasters.user_id==userformentry.user_id, FifthYearMasters.form_id==userformentry.form_id).first()
            fifthyearexamsneeded = db.session.query(FifthYearExamsNeeded).filter(FifthYearExamsNeeded.user_id==userformentry.user_id, FifthYearExamsNeeded.form_id==userformentry.form_id).first()
            endorsement = db.session.query(Endorsement).filter(Endorsement.user_id==userformentry.user_id, Endorsement.form_id==userformentry.form_id).first()
            practicumhistory = db.session.query(PracticumHistory).filter(PracticumHistory.user_id==userformentry.user_id, PracticumHistory.form_id==userformentry.form_id).first()
            practicumgrades = db.session.query(PracticumGrades).filter(PracticumGrades.user_id==userformentry.user_id, PracticumGrades.form_id==userformentry.form_id).first()
            
            if fifthyearexamsneeded is None:
                fifthyearexamsneeded = FifthYearExamsNeeded()
                
            if practicumgrades is None:
                practicumgrades = PracticumGrades()
                
            if practicumhistory is None:
                practicumhistory = PracticumHistory()

            
            print(os.getcwd())
            
                    
            #try:
                #return send_file('../myDump.csv', attachment_filename=fileName)
            with open('app/static/dump.csv', 'wb') as f:
                    
                fileName = str(data['3']) + '_fifthYear.csv'
                print('filename: ', fileName)
                csv.field_size_limit(500 * 1024 * 1024)
                out = csv.writer(f)
                    #out.writerow(['id', 'email'])
                    #for item in db.session.query(User).all():
                    #    out.writerow([item.id, item.email])
                    
                    
                    
                print('yargh')
                out.writerow(['Submission Date', 'Last Name', 'First Name', 'Term Graduating', 'Prefered County', 'Prefered Grade Level',
                                    'Endorsement Area', 'Exam Needed name', 'Examn Needed Date', 'Continue Study?', 'Reason for not Continuing',
                                    'Practicum School Name', 'Practicum School Division', 'Practicum Subject', 'Practicum Grade'])
                out.writerow([form.datesubmitted, user.last_name, user.first_name, fifthyear.termgraduating, fifthyear.preferedcountry, fifthyear.preferedgradelevel,
                                    endorsement.area, fifthyearexamsneeded.examname, fifthyearexamsneeded.examdate, fifthyearmasters.continuestudy, fifthyearmasters.reasonfordiscontinue,
                                    practicumhistory.schoolname, practicumhistory.schooldivision, practicumgrades.subject, practicumgrades.grade])
                    #out.writerow([fifthyearmasters.])
                    
                print('all done!')
                    #return jsonify({'status':'Success','filename':fileName, 'strcsv':strcsv})
                    
            #except:
		    #       return jsonify({'Failure':'Request was not valid.'})
                
            
            
            #return jsonify({'status':'Success','filename':fileName, 'strcsv':csv_file})
            return jsonify({'status':'Success','filename':fileName})


        
        #ai = ApplicationInformation.query.filter_by(name=data['button']).first()
        #ai.deadlineDate = data['date']
        
        #print(str(data['1']))
        
        #user = db.session.query(User).filter(User.email==str(data['1'])).first()
        #form = db.session.query(Forms).filter(Forms.user_id==user.id).first()
        #userformentry = db.session.query(UserForms).filter(form.user_id==UserForms.user_id, user.id==UserForms.form_id).first()
        
        #print(form.name)
        #db.session.delete(userformentry)
        #db.session.commit()

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
    
@admin.route('/exApplicationTable')
def exApplicationTable():
    """Return server side data."""
    
    print('stoff')
        
    print('creating application table')
    
    # defining columns
    columns = [
        ColumnDT(Forms.datesubmitted),
        ColumnDT(Forms.name),
        ColumnDT(User.email),
        ColumnDT(User.first_name),
        ColumnDT(User.last_name),
    ]
    
    print('params')
    
    params = request.args.to_dict()
    
    # defining the initial query depending on your purpose
    #query = db.session.query(User.id, User.email, User.first_name, User.last_name, User.lastLoginDate).filter(User.is_admin==False)
    query = db.session.query(Forms.datesubmitted, Forms.name, User.email, User.first_name, User.last_name).\
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
    
@admin.route('/delete', methods=['GET', 'POST'])
def delete():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! delete !')
    
   
    # load login template
    return render_template('admin/delete.html')
    
    
    
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