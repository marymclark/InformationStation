# app/forms/views.py

import datetime
from flask import request, flash, redirect, render_template, url_for, jsonify
from flask_login import login_required, current_user

from . import forms
from .. import db, helpers, models

# Data for Javascript

# Send endorsement data to Javascript
@forms.route('/data/endorsements')
@login_required
def getEndorsements():
    return jsonify(helpers.getEndorsements())

# Send school data to Javascript
@forms.route('/data/schools')
@login_required
def getSchools():
    return jsonify(helpers.getSchools())

# Continuation Form
@forms.route('/forms/continuation', methods=["GET","POST"])
@login_required
def continuationForm():
    if request.method == 'POST':
        try:
            data = request.get_json() # Get POSTed JSON from Javascript
        except:
            return jsonify({'status':'Failure','message':'No request data.'})
        print(data)
        
        # Check endorsement area
        for endorsement in data['endorsementArea']:
            endorsementArea = helpers.getEndorsementArea(endorsement)
            if (endorsementArea == 0):
                return jsonify({'status':'Failure','message':'An endorsement area is invalid.'})
                
        # Check the test requirements have valid tests and dates
        for item in data['testRequirements']:
            # TODO check date
            date = item['date']
            #if not (item['exam'] in ['Praxis','VCLA','RVE']):
            #    return jsonify({'status':'Failure','message':'A test requirement entry is invalid.'})
                
        # Check graduation
        checkGrad = data['graduation'].split()
        if not ((checkGrad[0] in ['May','August','December']) and (checkGrad[1] in helpers.nextnYears(5))):
            jsonify({'status':'Failure','message':'Invalid graduation month/year'})
            
        # Add data to database
        form = models.Forms(
            name = "Form_FifthYear",
            user_id=current_user.id,
            datesubmitted = datetime.date.today()
        )
        db.session.add(form)
        db.session.commit()
        
        userform = models.UserForms(
            user_id = current_user.id,
            form_id = form.id
        )
        db.session.add(userform)
        db.session.commit()
        
        endorsement = models.Endorsement(
            user_id = current_user.id,
            form_id = userform.form_id,
            area = endorsementArea
        )
        if len(data['testRequirements']) >= 1:
            exams = models.FifthYearExamsNeeded(
                user_id = current_user.id,
                form_id = userform.form_id,
                examname = data['testRequirements'][0]['exam'],
                examdate = data['testRequirements'][0]['date']
            )
            db.session.add(exams)
        masters = models.FifthYearMasters(
            user_id = current_user.id,
            form_id = userform.form_id,
            continuestudy = data['continue'],
            reasonfordiscontinue = data['reason']
        )
        finalform = models.Form_FifthYear(
            user_id = current_user.id,
            form_id = userform.form_id,
            #endorsementarea = endorsementArea,
            #examsneeded = exams.id,
            #mastersinfo = masters.id,
            #practicuminfo = practicum.id,
            termgraduating = data['graduation'],
            #preferedcountry = data['country'],
            #preferedgradelevel = data['level'],
        )
        
        db.session.add(endorsement)
        db.session.add(masters)
        #db.session.add(practicum)
        db.session.add(finalform)
        db.session.commit()
        
        return jsonify({'status':'Success','message':'Your form was submitted successfully!'})
    else:
        # Reason for not continuing
        reasons = ['Financial','Grades','Study Abroad','Moving out of Area','Personal','No longer interested in teaching','Other']
        return render_template("forms/continuation.html",years=helpers.nextnYears(5),reasons=reasons)

# Internship Form
@forms.route('/forms/internship', methods=["GET","POST"])
@login_required
def internshipForm():
    if request.method == 'POST':
        try:
            data = request.get_json() # Get POSTed JSON from Javascript
        except:
            return jsonify({'status':'Failure','message':'No request data.'})
        print(data)
        
        # Check endorsement area
        for endorsement in data['endorsementArea']:
            endorsementArea = helpers.getEndorsementArea(endorsement)
            if (endorsementArea == 0):
                return jsonify({'status':'Failure','message':'An endorsement area is invalid.'})
        
        # Add data to database
        form = models.Forms(
            user_id = current_user.id,
            name = "Form_FifthYear"
        )
        db.session.add(form)
        db.session.commit()
        
        userform = models.UserForms(
            user_id = current_user.id,
            form_id = form.id
        )
        db.session.add(userform)
        db.session.commit()
        
        
        return jsonify({'status':'Success','message':'Your form was submitted successfully!'})
    else:
        return render_template("forms/internship.html")

# Admission Form
@forms.route('/forms/admission', methods=["GET","POST"])
@login_required
def admissionForm():
    return render_template("forms/admission.html")