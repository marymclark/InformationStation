# app/forms/views.py

from flask import request, flash, redirect, render_template, url_for, jsonify
from flask_login import login_required, current_user

from . import forms
#from forms import
from .. import db, helpers 
from ..models import Forms, UserForms, Endorsement, Form_FifthYear, FifthYearMasters, FifthYearExamsNeeded, PracticumGrades

# Data for Javascript

# Send endorsement data to Javascript
@forms.route('/data/endorsements')
#@login_required
def getEndorsements():
    return jsonify(helpers.getEndorsements())

# Send school data to Javascript
@forms.route('/data/schools')
#@login_required
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
            return jsonify({'Failure':'No request data.'})
        print(data)
        
        # Check endorsement area
        for endorsement in data['endorsementArea']:
            endorsementArea = helpers.getEndorsementArea(endorsement)
            if (endorsementArea == 0):
                return jsonify({'Failure':'An endorsement area is invalid.'})
            else: print(endorsementArea)
                
        # Check the test requirements have valid tests and dates
        for item in data['testRequirements']:
            # TODO check date
            date = item['date']
            if not (item['exam'] in ['Praxis','VCLA','RVE']):
                return jsonify({'Failure':'A test requirement entry is invalid.'})
                
        # Check graduation
        checkGrad = data['graduation'].split()
        #if not ((checkGrad[0] in ['May','August','December']) and (checkGrad[1] in helpers.nextnYears(5))):
        #    return jsonify({'Failure':'Invalid graduation month/year'})
            
        # Add data to database
        form = Forms(
            name = "Form_FifthYear"
        )
        userform = UserForms(
            user_id = current_user.id,
            form_id = form.id
        )
        endorsement = Endorsement(
            user_id = current_user.id,
            form_id = form.id,
            area = endorsementArea
        )
        exams = FifthYearExamsNeeded(
            user_id = current_user.id,
            form_id = form.id,
            examname = data['testRequirements'][0]['exam'],
            examdate = data['testRequirements'][0]['date']
        )
        masters = FifthYearMasters(
            user_id = current_user.id,
            form_id = form.id,
            continuestudy = data['continue'],
            reasonfordiscontinue = data['reason']
        )
        #practicum = PracticumGrades(
        #    user_id = current_user.id,
        #    form_id = form.id,
        #    subject = data['practicum'][0]['grades']
        #)
        finalform = Form_FifthYear(
            user_id = current_user.id,
            form_id = form.id,
            endorsementarea = endorsementArea,
            examsneeded = exams.id,
            mastersinfo = masters.id,
            #practicuminfo = practicum.id,
            termgraduating = data['graduation'],
            preferedcountry = data['country'],
            preferedgradelevel = data['level'],
        )
        
        db.session.add(form)
        db.session.add(userform)
        db.session.add(endorsement)
        db.session.add(exams)
        db.session.add(masters)
        db.session.add(practicum)
        db.sessoin.add(finalform)
        
        db.session.commit()
        
        # For now, return success when valid 
        return jsonify({'Success':'Request was valid.'})
    else:
        # Reason for not continuing
        reasons = ['Financial','Grades','Study Abroad','Moving out of Area','Personal','No longer interested in teaching','Other']
        return render_template("forms/continuation.html",years=helpers.nextnYears(5),reasons=reasons)

# Internship Form
@forms.route('/forms/internship', methods=["GET","POST"])
#@login_required
def internshipForm():
    return render_template("forms/internship.html")

# Admission Form
@forms.route('/forms/admission', methods=["GET","POST"])
@login_required
def admissionForm():
    return render_template("forms/admission.html")