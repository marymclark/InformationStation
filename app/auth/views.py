# app/auth/views.py

from datetime import date

from flask import flash, redirect, render_template, url_for, abort
from flask_login import login_required, login_user, logout_user
from sqlalchemy import update

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User
from ..utils import send_email, ts

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    
    error=''
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)
                            
        print('confirm: ', user.email)
        print(user.email[-13:])
                            
        if (user.email[-13:] != '@mail.umw.edu'):
            print('NEGATIVE')
            error = error + 'Please enter a valid UMW email ending in @mail.umw.edu'
        else:
            # add new user to the database
            db.session.add(user)
            db.session.commit()
        
            # Now we'll send the email confirmation link
            subject = "Confirm your email"
            token = ts.dumps(user.email, salt='email-confirm-key')
        
            confirm_url = url_for(
                'auth.confirm_email',
                token=token,
                _external=True)

            html = render_template(
                'email/activate.html',
                confirm_url=confirm_url)

            # Let's assume that send_email was defined in myapp/util.py
            send_email(subject, 'no-reply@coeas', user.email, html)
        
            flash('You have successfully registered! Please confirm your email before logging in.')

            # redirect to the login page
            return redirect(url_for('auth.login'))

    # load registration template
    print('we reroute')
    
    return render_template('auth/register.html', form=form, title='Register', error=error)
    
@auth.route('/confirm/<token>', methods=["GET", "POST"])
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.confirmed = True
    
    print('User email confirmed!')

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log employee in
            if user.confirmed == False:
                flash('Please confirm your Email before logging in.')
            else:
                login_user(user)
            
                day = date.today() #for updating recent login time
            
                print('UPDATE DATE: ', str(user.email), str(day))
                user.lastLoginDate = day
                print(user.lastLoginDate)
                db.session.commit()

                # redirect to the dashboard page after login
                if user.is_admin:
                    return redirect(url_for('home.admin_dashboard'))
                else:
                    return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))