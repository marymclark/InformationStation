# app/home/views.py

from flask import abort, render_template, url_for, redirect
from flask_login import current_user, login_required

from . import home

from forms import EmailForm
from .. import db
from ..models import User
from ..utils import send_email, ts

# Index
@home.route('/')
def index():
    
    return render_template("home/index.html")
    
    
@home.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"
        print(subject)

        # Here we use the URLSafeTimedSerializer we created in `util` at the
        # beginning of the chapter
        token = ts.dumps(user.email, salt='recover-key')

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'email/recover.html',
            recover_url=recover_url)

        # Let's assume that send_email was defined in myapp/util.py
        #send_email(user.email, subject, html)

        return redirect(url_for('home.index'))
    return render_template('home/reset.html', form=form)
    
@home.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('auth.login'))
    
    
# User Dashboard
@home.route('/dashboard')
@login_required
def dashboard():
    
    return render_template("home/userdash.html")
    
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")