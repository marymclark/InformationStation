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
    #endorsememtid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area = db.Column(db.String(60), index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
    
class PracticumGrades(UserMixin, db.Model):

    __tablename__ = 'practicumgrades'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgradesid = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    subject = db.Column(db.String(60), index=True)
    grade = db.Column(db.Integer, index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class PracticumHistory(UserMixin, db.Model):

    __tablename__ = 'practicumhistory'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    schoolname = db.Column(db.String(60), index=True)
    schooldivision = db.Column(db.String(60), index=True)


    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class PostbacRelationships(UserMixin, db.Model):

    __tablename__ = 'postbacrelationships'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    personname = db.Column(db.String(60), index=True)
    schoolname = db.Column(db.String(60), index=True)
    relationshiptype = db.Column(db.String(128), index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)

    
class Form_Postbac(UserMixin, db.Model):

    __tablename__ = 'form_postbac'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    preferedcountry = db.Column(db.String(120), index=True)
    preferedgradelevel = db.Column(db.Integer, index=True)
    requirementssatisfied = db.Column(db.Boolean, index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
    
#####################################################################################################

class FifthYearExamsNeeded(UserMixin, db.Model):

    __tablename__ = 'fifthyearexamsneeded'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    examname = db.Column(db.String(60), index=True)
    examdate = db.Column(db.Date, index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class FifthYearMasters(UserMixin, db.Model):

    __tablename__ = 'fifthyearmasters'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    continuestudy = db.Column(db.Boolean, index=True)
    reasonfordiscontinue = db.Column(db.String(128), index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class Form_FifthYear(UserMixin, db.Model):

    __tablename__ = 'form_fifthyear'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    termgraduating = db.Column(db.String(60), index=True)
    preferedcountry = db.Column(db.String(120), index=True)
    preferedgradelevel = db.Column(db.Integer, index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)

###################################################################################################################################

class TransferInfo(UserMixin, db.Model):

    __tablename__ = 'transferinfo'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    collegename = db.Column(db.String(60), index=True)
    collegecity = db.Column(db.String(120), index=True)
    collegestate = db.Column(db.String(120), index=True)
    startdate= db.Column(db.Date, index=True)
    enddate = db.Column(db.Date, index=True)
    preferedgradelevel = db.Column(db.Integer, index=True)
    degreeearned = db.Column(db.String(60), index=True)
    enrolledname = db.Column(db.String(60), index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class LeadershipHistory(UserMixin, db.Model):

    __tablename__ = 'leadershiphistory'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    positionheld = db.Column(db.String(60), index=True)
    positiondescription = db.Column(db.String(120), index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class YouthHistory(UserMixin, db.Model):

    __tablename__ = 'youthhistory'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    positionheld = db.Column(db.String(60), index=True)
    positiondescription = db.Column(db.String(120), index=True)

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class StudentInformation(UserMixin, db.Model):

    __tablename__ = 'studentinformation'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    umwstatus = db.Column(db.String(60), index=True)
    studenttype = db.Column(db.String(120), index=True)
    majorprogram = db.Column(db.String(60), index=True)
    declared = db.Column(db.Boolean, index=True)
    majoradvisor = db.Column(db.String(66), index=True)
    monthyeargrad = db.Column(db.String(60), index=True)
    accumulatedcredithours = db.Column(db.Integer, index=True)
    informationsessionattendancedate = db.Column(db.Date, index=True)
    applieddate = db.Column(db.Date, index=True)
    preferedgender = db.Column(db.String(30), index=True)
    birthday = db.Column(db.Date, index=True)
    preferedrace = db.Column(db.String(30), index=True)
    

    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)
    
class Form_UndergradAdmission(UserMixin, db.Model):

    __tablename__ = 'form_undergradadmission'

    user_id = db.Column(db.Integer, db.ForeignKey('userforms.user_id'), primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('userforms.form_id'), primary_key=True)
    #practicumgrades = db.Column(db.Integer, db.ForeignKey('practicumgrades.practicumgradesid'), primary_key=True)
    bannerid = db.Column(db.String(9), index=True)
    localaddress = db.Column(db.String(120), index=True)
    campusphonenumber = db.Column(db.String(12), index=True)
    permanentaddress = db.Column(db.String(120), index=True)
    permanentphonenumber = db.Column(db.String(12), index=True)
    


    #def __repr__(self):
    #    return '<User: {}>'.format(self.email)