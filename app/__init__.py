# File to initialize the application

from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
import helpers

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."


@login_manager.user_loader
def load_user(user_id):
    return helpers.User.get(user_id)

# Uncomment this in production
# application = app

# Load the views
from app import views, models, controllers

# Load the config file
app.config.from_object('config')

app.secret_key = "not so secret"

#db = SQLAlchemy(app)
#db.init_app(app)