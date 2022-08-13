from itsdangerous import URLSafeTimedSerializer
from flask import render_template, current_app
import requests

from app.models import User
from app.services.email import Email

class InvalidRegistration(Exception):
    #StandardError
    pass
class EmailProviderError(Exception):
    #StandardError
    pass

class VerifyRegistration:
# Error for invalid registration details

    def __init__(self, registration):
        self.registration = registration

    def call(self):
        if not self.username_available():
            raise(InvalidRegistration, 'Username exists')
        
        if not self.email_available():
            raise(InvalidRegistration, 'Email already used')

        Email(self.registration).send_email_verification()

    def username_available(self):
        return User.query.filter_by(username = self.registration["username"]).first is not None

    def email_available(self):
        return User.query.filter_by(email = self.registration["email"]).first is not None

    """rescue StandardError
        raise(InvalidRegistration,
            'Could not send verification email; please check email address')"""
