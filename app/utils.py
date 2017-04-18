# app/utils.py

import flask

from flask_mail import Message
from app import mail

from itsdangerous import URLSafeTimedSerializer

ts = URLSafeTimedSerializer(flask.current_app.config["SECRET_KEY"])

#def send_email(subject, sender, recipients, text_body, html):
def send_email(subject, sender, recipients, html):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = 'Hello!'
    #msg.html = html
    print('arr:', subject, sender, recipients)
    
    print('sendto: ', str(recipients))
    
    msg = Message(subject,
                  sender="from@example.com",
                  recipients=[str(recipients)])
                  
    msg.html=html
    
    try:
        mail.send(msg)
        print('mail sent!')
    except:
        print('mail did a fail!')