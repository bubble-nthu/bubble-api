from flask import render_template, current_app
import requests
from flask import render_template, current_app
from flask_mail import Message

from .. import mail

from app.models import User

class InvalidRegistration(Exception):
    #StandardError
    pass
class EmailProviderError(Exception):
    #StandardError
    pass

class Email:
    def __init__(self, setting):
        self.setting = setting
        self.mail_url = current_app.config['MAIL_API_URL']
        self.from_email = current_app.config['MAIL_SENDER']
        self.mail_api_key = current_app.config['MAIL_API_KEY']
        self.html_email = render_template('auth/email/confirm' + '.html', username = self.setting["username"], 
                                            register_url = self.setting["verification_url"])

    def mail_json(self):
        msg = {
            "personalizations": [
                {
                "to": [{ 'email': self.setting["email"] }]
            }],
            "from": { 'email': self.from_email },
            "subject": '帳號註冊驗證信｜Bubble',
            "content": [
                { "type": 'text/html',
                "value": self.html_email }
            ]
        }
        return msg

    def send_email_verification(self):
        hed = {'Authorization': f'Bearer {self.mail_api_key}'}
        response = requests.post(self.mail_url, json=self.mail_json(), headers=hed)
        if response.status_code >= 300:
            raise EmailProviderError

    @classmethod
    def send(to, subject, template, **kwargs):
        msg = Message(subject, sender=current_app.config['MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)