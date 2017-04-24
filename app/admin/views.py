# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for, request, jsonify, send_file, json
from flask_login import current_user, login_required
from functools import wraps
import csv
import io
import os
from StringIO import StringIO

from datatables import ColumnDT, DataTables

from . import admin
from .. import db
from ..models import User, ApplicationInformation, Forms, UserForms, Form_FifthYear, FifthYearMasters, FifthYearExamsNeeded, Endorsement, PracticumHistory, PracticumGrades

"""
Prevent non-admins from accessing the page
"""
def admin_required(func):
    @wraps(func)
    def check_admin_and_call(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return check_admin_and_call
  
@admin.route('/deleteUser', methods=['POST'])
@admin_required
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
        
        try:
        
            user = db.session.query(User).filter(User.email==str(data['1'])).first()
            db.session.delete(user)
            db.session.commit()

            return jsonify({'status':'Success','message':'Deleting successful!'})
            
        except:
            return jsonify({'status':'Failure','message':'There is a form submitted by this user.!'})
        
        
@admin.route('/delApplication', methods=['POST'])  
@admin_required
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
        
        print(str(data['2']))
        
        user = db.session.query(User).filter(User.email==str(data['3'])).first()
        form = db.session.query(Forms).filter(Forms.user_id==user.id).first()
        userformentry = db.session.query(UserForms).filter(form.user_id==UserForms.user_id, user.id==UserForms.form_id).first()
        
        if str(data['2'] == 'Form_FifthYear'):
            print(userformentry.user_id, ' ', userformentry.form_id)
            fifthyear = db.session.query(Form_FifthYear).filter(Form_FifthYear.user_id==userformentry.user_id, Form_FifthYear.form_id==userformentry.form_id).first()
            #print(fifthyear.termgraduating)
            fifthyearmasters = db.session.query(FifthYearMasters).filter(FifthYearMasters.user_id==userformentry.user_id, FifthYearMasters.form_id==userformentry.form_id).first()
            fifthyearexamsneeded = db.session.query(FifthYearExamsNeeded).filter(FifthYearExamsNeeded.user_id==userformentry.user_id, FifthYearExamsNeeded.form_id==userformentry.form_id).first()
            endorsement = db.session.query(Endorsement).filter(Endorsement.user_id==userformentry.user_id, Endorsement.form_id==userformentry.form_id).first()
            practicumhistory = db.session.query(PracticumHistory).filter(PracticumHistory.user_id==userformentry.user_id, PracticumHistory.form_id==userformentry.form_id).first()
            practicumgrades = db.session.query(PracticumGrades).filter(PracticumGrades.user_id==userformentry.user_id, PracticumGrades.form_id==userformentry.form_id).first()
            if fifthyear:
                db.session.delete(fifthyear)
                print('del fifthyear')
                db.session.commit()
            if fifthyearmasters:
                print('del fifthyearmasters')
                db.session.delete(fifthyearmasters)
                db.session.commit()
            if fifthyearexamsneeded:
                print('del fifthyearexamsneeded')
                db.session.delete(fifthyearexamsneeded)
                db.session.commit()
            if endorsement:
                print('del endorsement')
                db.session.delete(endorsement)
                db.session.commit()
            if practicumhistory:
                print('del practicumhistory')
                db.session.delete(practicumhistory)
                db.session.commit()
            if practicumgrades:
                print('del practicumgrades')
                db.session.delete(practicumgrades)
                db.session.commit()
                
            if userformentry:
                print('del userform')
                db.session.delete(userformentry)
                db.session.commit()
            
            if form:
                print('del form')
                Forms.query.filter_by(id=form.id).delete()
                db.session.commit()
            
            #print(form.name)

        return jsonify({'Success':'Request was valid.'})
    
    
        
@admin.route('/exApplication', methods=['POST'])  
@admin_required
def exApplication():
    
    
    
    print('exporting dat app!')
    
    if request.method == 'POST':
        try:
            data = request.get_json() # Get POSTed JSON from Javascript
        except:
            return jsonify({'Failure':'No request data.'})
            
        numFifthYear = 0
        numBacs = 0
        numUndergrad = 0
        
        fifthyears = []
        postbacs = []
        undergrads = []
            
        print(data)
        print(data[0]['2'])
        print('data: ', data[0])
        
        for d in data:
            if (d['2'] == 'Form_FifthYear'):
                fifthyears.append(d)
            if (d['2'] == 'Form_Post-bac'):
                postbacs.append(d)
                
        print('len fifthyear: ', len(fifthyears))
        
        print(fifthyears)
        
        if len(fifthyears) > 0:
            #with open('app/static/dump.csv', 'wb') as f:
            fileName = 'fifthYear.csv'
            print('filename: ', fileName)
            f  = open('app/static/' + fileName, 'wb') 
            csv.field_size_limit(500 * 1024 * 1024)
            out = csv.writer(f)
                    
            print('yargh')
            out.writerow(['Submission Date', 'Last Name', 'First Name', 'Term Graduating', 'Prefered County', 'Prefered Grade Level',
                                'Endorsement Area', 'Exam Needed name', 'Examn Needed Date', 'Continue Study?', 'Reason for not Continuing',
                                'Practicum School Name', 'Practicum School Division', 'Practicum Subject', 'Practicum Grade'])
    
        #Form_FifthYear, FifthYearMasters, FifthYearExamsNeeded, Endorsement, PracticumHistory
        #EXPORT FIFTHYEAR FORM
        for thisform in fifthyears:
            user = db.session.query(User).filter(User.email==str(thisform['3'])).first()
            print('user email: ', str(thisform['3']))
            print('formid:', int(thisform['0']))
            form = db.session.query(Forms).filter(Forms.user_id==user.id, Forms.id==int(thisform['0'])).first()
            
            fileName = 'fifthYear.csv'
        
            print('date: ', form.datesubmitted)
        
            print('userEmail: ', user.email)
            print('formName: ', form.name)
            userformentry = db.session.query(UserForms).filter(UserForms.user_id==form.user_id, UserForms.form_id==form.id).first()
            print(str(userformentry.user_id), ' ', str(userformentry.form_id))
            
            print('form: ', form)
            fifthyear = db.session.query(Form_FifthYear).filter(Form_FifthYear.user_id==userformentry.user_id, Form_FifthYear.form_id==userformentry.form_id).first()
            print(fifthyear.termgraduating)
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
            
            print('termtest:', fifthyear.termgraduating)
            
                    
            #try:
                #return send_file('../myDump.csv', attachment_filename=fileName)
            with open('app/static/fifthYear.csv', 'a') as f:
                
                csv.field_size_limit(500 * 1024 * 1024)
                out = csv.writer(f)
                
                print('file open')
                    
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
@admin_required
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
@admin_required
def delApplicationTable():
    """Return server side data."""
    
    print('stoff')
        
    print('creating application table')
    
    # defining columns
    columns = [
        ColumnDT(Forms.id),
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
    query = db.session.query(Forms.id, Forms.datesubmitted, Forms.name, User.email, User.first_name, User.last_name).\
        filter(User.id==Forms.user_id)
    print('query: ', query)
    
    params = request.args.to_dict()
    
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())
    
@admin.route('/exApplicationTable')
@admin_required
def exApplicationTable():
    """Return server side data."""
    
    print('stoff')
        
    print('creating application table')
    
    # defining columns
    columns = [
        ColumnDT(Forms.id),
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
    query = db.session.query(Forms.id, Forms.datesubmitted, Forms.name, User.email, User.first_name, User.last_name).\
        filter(User.id==Forms.user_id)
    print('query: ', query)
    
    params = request.args.to_dict()
    
    # instantiating a DataTable for the query and table needed
    rowTable = DataTables(params, query, columns)
    
    # returns what is needed by DataTable
    return jsonify(rowTable.output_result())
    
    
@admin.route('/userTable')
@admin_required
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
@admin_required
def database():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! database !')
    
   
    # load login template
    return render_template('admin/database.html')
    
@admin.route('/users', methods=['GET', 'POST'])
@admin_required
def users():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! users !')
    
   
    # load login template
    return render_template('admin/users.html')
    
    
@admin.route('/export', methods=['GET', 'POST'])
@admin_required
def export():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! export !')
    
   
    # load login template
    return render_template('admin/export.html')
    
@admin.route('/delete', methods=['GET', 'POST'])
@admin_required
def delete():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! delete !')
    
   
    # load login template
    return render_template('admin/delete.html')
    
    
    
@admin.route('/deadlines', methods=['GET', 'POST'])
@admin_required
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
@admin_required
def index():
 
    #if request.method == 'POST':
    #    print('yAsssss')
    #    return
    
    print('Inside ! admin ! dashboard !')
    
   
    # load login template
    return render_template('admin/admin_dashboard.html')