from flask import current_app
from flask_mail import Message

from api import mail


def send_mail(subject, body, recipient):
    if current_app.config['TESTING']:
        return

    message = Message(
        subject=subject,
        body=body,
        recipients=[recipient],
        sender=('Ziramba', 'noreply@ziramba.com')
    )

    mail.send(message=message)
    return
