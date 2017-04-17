# app/utils.py

import flask

from flask_mail import Message
from app import mail

from itsdangerous import URLSafeTimedSerializer

ts = URLSafeTimedSerializer(flask.current_app.config["SECRET_KEY"])

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)