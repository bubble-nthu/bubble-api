from flask import render_template, current_app
from flask_mail import Message

from .. import mail

class Email():

    @staticmethod
    def send(to, subject, template, **kwargs):
        msg = Message(subject, sender=current_app.config['MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)