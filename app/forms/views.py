# app/forms/views.py
import datetime

from flask import request, flash, redirect, render_template, url_for, jsonify
from flask_login import login_required, current_user

from . import forms
#from forms import
from .. import db, helpers
from .. import models

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
        
        # Check endorsement area
        endorsementArea = []
        for endorsement in data['endorsementArea']:
            area = helpers.getEndorsementArea(endorsement)
            if (endorsementArea == 0):
                return jsonify({'status':'Failure','message':'An endorsement area is invalid.'})
            else:
                endorsementArea.append(area)
                
        # Check the test requirements have valid tests and dates?
        # for item in data['testRequirements']:
        #     date = item['date']
        #     if not (item['exam'] in ['Praxis','VCLA','RVE']):
        #         return jsonify({'status':'Failure','message':'A test requirement entry is invalid.'})
                
        # Check graduation
        checkGrad = data['graduation'].split()
        if not ((checkGrad[0] in ['May','August','December']) and (checkGrad[1] in helpers.nextnYears(5))):
            jsonify({'status':'Failure','message':'Invalid graduation month/year'})
            
        # Add data to database
        form = models.Forms(
            name = "Form_FifthYear",
            user_id=current_user.id,
            #datesubmitted = datetime.date.today()
            datesubmitted = datetime.datetime.now()
        )
        db.session.add(form)
        db.session.commit()
        
        userform = models.UserForms(
            user_id = current_user.id,
            form_id = form.id
        )
        db.session.add(userform)
        db.session.commit()
        
        for item in endorsementArea:
            endorsement = models.Endorsement(
                user_id = current_user.id,
                form_id = userform.form_id,
                area = item
            )
            db.session.add(endorsement)
            db.session.commit()
        for item in data['testRequirements']:
            exam = models.FifthYearExamsNeeded(
                user_id = current_user.id,
                form_id = userform.form_id,
                examname = item['exam'],
                examdate = item['date']
            )
            db.session.add(exam)
            db.session.commit()
        masters = models.FifthYearMasters(
            user_id = current_user.id,
            form_id = userform.form_id,
            continuestudy = data['continue'],
            reasonfordiscontinue = data['reason']
        )
        finalform = models.Form_FifthYear(
            user_id = current_user.id,
            form_id = userform.form_id,
            termgraduating = data['graduation'],
            #preferedcountry = data['country'],
            #preferedgradelevel = data['level'],
        )
        
        db.session.add(masters)
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
        
        # Check endorsementarea
        endorsementArea = []
        for endorsement in data['endorsementArea']:
            area = helpers.getEndorsementArea(endorsement)
            if (endorsementArea == 0):
                return jsonify({'status':'Failure','message':'An endorsement area is invalid.'})
            else:
                endorsementArea.append(area)
        
        # Add data to database
        form = models.Forms(
            user_id = current_user.id,
            name = "Form_Postbac",
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
        
        for item in endorsementArea:
            endorsement = models.Endorsement(
                user_id = current_user.id,
                form_id = userform.form_id,
                area = item
            )
            db.session.add(endorsement)
            db.session.commit()
        for item in data['practicums']:
            grade = models.PracticumGrades(
                user_id = current_user.id,
                form_id = userform.form_id,
                subject = item['subject'],
                grade = item['grade']
            )
            db.session.add(grade)
            practicum = models.PracticumHistory(
                user_id = current_user.id,
                form_id = userform.form_id,
                practicumgrades = grade.id,
                schoolname = item['school'],
                schooldivision = item['division']
            )
            db.session.add(practicum)
            db.session.commit()
        for item in data['relationships']:
            relationship = models.PostbacRelationships(
                user_id = current_user.id,
                form_id = userform.form_id,
                personname = item['name'],
                schoolname = item['school'],
                relationshiptype = item['rel']
            )
            db.session.add(relationship)
            db.session.commit()
        finalform = models.Form_Postbac(
            user_id = userform.user_id,
            form_id = userform.form_id,
            #preferedcountry = None,
            #preferedgradelevel = None,
            requirementssatisfied = data['tests']
        )
        
        db.session.add(finalform)
        db.session.commit()
        
        return jsonify({'status':'Success','message':'Your form was submitted successfully!'})
    else:
        return render_template("forms/internship.html")

# Admission Form
@forms.route('/forms/admission', methods=["GET","POST"])
@login_required
def admissionForm():
    return render_template("forms/admission.html")