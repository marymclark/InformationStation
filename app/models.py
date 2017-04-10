from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager 

class User(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    lastLoginDate = db.Column(db.DateTime, index=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.email)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    
    
class Forms(UserMixin, db.Model):
    """
    Forms connections form id to form name
    """

    __tablename__ = 'forms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), index=True)

class UserForms(UserMixin, db.Model):
    """
    User-Form join table (Connects users to their submitted forms)
    """

    __tablename__ = 'userforms'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('forms.id'), primary_key=True)
    
class Endorsement(UserMixin, db.Model):
    """
    Endorsement area table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'endorsement'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    area = db.Column(db.String(60), index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)