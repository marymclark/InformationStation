# app/auth/__init__.py

from flask import Blueprint

forms = Blueprint('forms', __name__)

from . import views