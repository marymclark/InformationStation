# -*- coding: utf-8 -*-
import os
import sys
import uuid
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from functools import wraps
from forms import *
from auth import *

# App Initialization
app = Flask(__name__)
app.secret_key = os.urandom(24).encode('hex')
socketio = SocketIO(app)

users = dict()

# Application Settings
app.config['USER_PHOTOS'] = 'static/data/img/'
app.config['USER_RESUMES'] = 'static/data/resume/'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

messages = []


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for("_login"))
        return f(*args, **kwargs)
    return decorated_function


@SocketIO.on(socketio, 'connect', namespace='/')
def sock_connect():
    prev_messages = get_messages()
    messages = []
    for m in prev_messages:
        messages.append({'author': m['author'],
                         'txt': m['text'],
                         'time': str(m['ts'])})
    for m in messages:
        emit('message', m)


@SocketIO.on(socketio, 'message', namespace='/')
@login_required
def sock_message(m):
    message = {
        'author': users[session['uuid']]['username'],
        'txt': m,
        'time': str(datetime.now())
    }
    insert_message(message)
    messages.append(message)
    emit('message', message, broadcast=True)


# @flask_socketio.SocketIO.on(socketio, 'message', namespace='/')
# def sock_message():
#     session['uuid'] = uuid.uuid1()
#     session['username'] = 'New User'
#     users[session['uuid']] = {'username', session['username']}


@app.route("/dashboard", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def _index():
    form = EditProfileForm(request.form)
    if 'user' in session:
        if request.method == 'GET':
            return render_template('dashboard.html', form=form)
        if request.method == 'POST' and form.validate():
            return render_template('edit.html', form=form)
    else:
        return render_template('index.html')


@app.route("/register")
def _register():
    return render_template('register.html')


@app.route('/new-student', methods=['GET', 'POST'])
def _register_student():
    alert = {0: ['success', 'Account created successfully!'],
             1: ['danger', 'An error occurred creating your student account.'],
             2: ['danger', 'An error occurred creating your user account.'],
             3: ['danger', 'Sorry, that username is taken.'],
             4: ['danger', 'An unexpected error occurred.']}
    form = StudentRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = dict(username=form.username.data, email=form.email.data, first=form.first.data, middle=form.middle.data,
                    last=form.last.data, password=form.password.data)
        code = add_student(user)
        if code != 0:
            if code in [1, 2, 3]:
                return render_template('register-student.html', form=form, alert=alert[code][1], alert_code=alert[code][0])
            else:
                return render_template('register-student.html', form=form, alert=alert[4][1], alert_code=alert[4][0])
        return _login(['success', 'Account created successfully, taking you to your dashboard!'], True)
    return render_template('register-student.html', form=form)


@app.route('/new-employer', methods=['GET', 'POST'])
@login_required
def _register_employer():
    alert = {0: ['success', 'Account created successfully!'],
             1: ['danger', 'An error occurred creating your employer account.'],
             2: ['danger', 'An error occurred creating your user account.'],
             3: ['danger', 'An unexpected error occurred.']}
    form = EmployerRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = dict(name=form.username.data, company=form.company.data, email=form.email.data,
                    password=form.password.data)
        code = add_employer(user)
        if code != 0:
            if code in [1, 2]:
                return render_template('index.html', alert=alert[code][1], alert_code=alert[code][0])
            else:
                return render_template('index.html', alert=alert[3][1], alert_code=alert[3][0])
        return render_template('login.html', alert=alert[0][1], alert_code=alert[0][0])
    return render_template('register-employer.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def _login(prior_alert=None, new_acct=False):
    alert = {0: ['success', 'Login successful!'],
             1: ['danger', 'Sorry, invalid username / password combination.'],
             2: ['danger', 'Sorry, invalid username / password combination.'],
             3: ['danger', 'A server error occurred! Please try again later!'],
             4: ['danger', 'An unexpected error occurred.']}
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        credentials = {'username': form.username.data,
                       'password': form.password.data}
        code = login(credentials)
        if code != 0:
            if code in [1, 2, 3]:
                return render_template('login.html', form=form, alert=alert[code][1], alert_code=alert[code][0])
            else:
                return render_template('login.html', form=form, alert=alert[4][1], alert_code=alert[4][0])
        else:
            session['uuid'] = uuid.uuid1()
            users[session['uuid']] = {'username': session['user']['username']}
            print(users)
            form = EditProfileForm(request.form)
            if new_acct:
                return render_template('/dashboard.html', form=form, alert=prior_alert[1], alert_code=prior_alert[0])
            return render_template('/dashboard.html', alert=alert[0][1], alert_code=alert[0][0], form=form)
    if prior_alert is None:
        return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form, alert=prior_alert[1], alert_code=prior_alert[0])


def debug(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print session['user']
        return f(*args, **kwargs)
    return decorated_function


@app.route('/logout', methods=['GET', 'POST'])
def _logout():
    session.clear()
    form = LoginForm(request.form)
    return render_template('login.html', form=form, alert='You have successfully logged out!', alert_code='success')


@app.route("/edit-profile")
@app.route('/edit', methods=['GET', 'POST'])
@login_required
@debug
def _edit():
    alert = {0: ['success', 'Profile updated successfully!'],
             1: ['info', 'Edit your profile directly from the dashboard!'],
             2: ['danger', 'Sorry, allowed image file extensions are: png, jpg, and gif'],
             3: ['danger', 'There was a problem updating one or more fields'],
             4: ['danger', 'There was a problem uploading your file'],
             5: ['danger', 'A server-side error occurred'],
             6: ['danger', 'Sorry, resumes should be in PDF format only']}
    form = EditProfileForm(request.form)
    if request.method == 'GET':
        return render_template('dashboard.html', form=form, alert=alert[1][1], alert_code=alert[1][0])
    if request.method == 'POST' and form.validate():
        changes = dict(first_name=form.first.data,
                       middle_name=form.middle.data,
                       last_name=form.last.data,
                       email_address=form.email.data,
                       phone_number=form.phone.data,
                       link_linkedin=form.linkedin.data,
                       link_website=form.website.data,
                       bio=form.bio.data,
                       tag_line=form.tagline.data)
        print changes
        print form.profile_img.data
        profile_img = None
        filename = None
        if 'profile_img' in request.files:
            profile_img = request.files['profile_img']
        if profile_img and profile_img.filename == '':
            profile_img = None
        if profile_img:
            if verify_photo(profile_img.filename):
                filename = generate_filename(profile_img.filename)
                filename = os.path.join(app.config['USER_PHOTOS'], filename)
                print(filename)
                profile_img.save(filename)
                profile_img = filename
            else:
                return render_template('dashboard.html', form=form, alert=alert[2][1], alert_code=alert[2][0])
        resume = None
        filename = None
        if 'resume' in request.files:
            resume = request.files['resume']
        if resume and resume.filename == '':
            resume = None
        if resume:
            if verify_resume(resume.filename):
                filename = generate_filename(resume.filename)
                filename = os.path.join(app.config['USER_RESUMES'], filename)
                print(filename)
                resume.save(filename)
                resume = filename
            else:
                return render_template('dashboard.html', form=form, alert=alert[6][1], alert_code=alert[6][0])
        if changes['link_linkedin'] and len(changes['link_linkedin']) > 0 \
                and not changes['link_linkedin'].startswith('http://'):
            changes['link_linkedin'] = 'http://' + changes['link_linkedin']
        if changes['link_website'] and len(changes['link_website']) > 0 \
                and not changes['link_website'].startswith('http://'):
            changes['link_website'] = 'http://' + changes['link_website']
        code = update_profile(changes, profile_img, resume)
        return render_template('dashboard.html', form=form, alert=alert[code][1], alert_code=alert[code][0])


@app.route("/guide")
@app.route("/student-guide")
def _guide():
    form = EditProfileForm(request.form)
    return render_template('guide-student.html', form=form)


@app.route("/edit-position")
def _edit_position():
    return render_template('edit-position.html')


@app.route("/search")
def _search():
    return render_template('search.html')


@app.route("/e/<emp_name>")
def _employer():
    return render_template('profile.html')


@app.route("/s/<student_name>")
def _student():
    return render_template('profile.html')


@app.route("/p/<pos_name>")
def _position():
    return render_template('position.html')


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '8080')), debug=True)
