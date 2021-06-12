import os

from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer


from api import mail

SECRET_KEY = os.getenv('SECRET_KEY')
SECURITY_SALT = os.getenv('SECURITY_SALT')


def send_mail(subject, body, recipient):
    if current_app.config['TESTING']:
        return

    message = Message(
        subject=subject,
        body=body,
        recipients=[recipient],
        sender=(os.getenv('MAIL_SENDER'), os.getenv('MAIL_USERNAME'))
    )

    mail.send(message=message)
    return


def get_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_SALT)


def verify_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(SECRET_KEY)

    try:
        email = serializer.loads(token, salt=SECURITY_SALT, max_age=expiration)

    except:
        return None

    return email
