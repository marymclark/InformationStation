# File to initialize the application

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_assets import Environment, Bundle

#import helpers
from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()
mail= Mail()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    # SQL settings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    migrate = Migrate(app, db) # says it's unused; do we need this here?
    
    # Login Manager and quick_forms
    Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    
    # Compile assets
    assets = Environment(app)
    # Compile and register js bundle
    js_bundle = Bundle(
        'vendor/jquery/jquery.min.js',
        'vendor/bootstrap/bootstrap.min.js',
        Bundle('js/freelancer.js','js/custom.js',
                filters = 'jsmin'),
        output = 'gen/compiled.js')
    assets.register('js_all', js_bundle)
    # Compile and register css bundle
    css_bundle = Bundle(
        Bundle('vendor/bootstrap/bootstrap.min.css','css/custom.css',
                filters = ['cssmin']),
        Bundle('less/mixins.less','less/variables.less','less/freelancer.less',
                filters = ['less','cssmin']),
        output = 'gen/compiled.css')
    assets.register('css_all', css_bundle)
    
    # Configure mail settings
    mail = Mail(app)
    app.config.update(
    	DEBUG=True,
    	#EMAIL SETTINGS
    	MAIL_SERVER='smtp.gmail.com',
    	MAIL_PORT=465,
    	MAIL_USE_SSL=True,
    	MAIL_USERNAME = 'coeas.email@gmail.com',
    	MAIL_PASSWORD = 'coedevteam'
	)
    mail.init_app(app)

    from app import models # Unused -- does this need to be here?
    with app.app_context():
        from .admin import admin as admin_blueprint
        app.register_blueprint(admin_blueprint, url_prefix='/admin')

        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .home import home as home_blueprint
        app.register_blueprint(home_blueprint)
    
        from .forms import forms as forms_blueprint
        app.register_blueprint(forms_blueprint)

    return app