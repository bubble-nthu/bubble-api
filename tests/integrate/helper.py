# content of tests/conftest.py
import pytest
from base64 import b64encode
import json
import re
from base64 import b64encode
from app import db
from app.models import User, Role

def get_basic_api_headers(email, password):
    return {
        'Authorization': 'Basic ' + b64encode(
            (email + ':' + password).encode('utf-8')).decode('utf-8'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

def get_bearer_api_headers(token):
    return {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

def add_user(email, password, username,confirmed=True, role="User"):
    # add a user
    r = Role.query.filter_by(name=role).first()
    u = User(email=email, password=password, username=username, confirmed=confirmed,
                role=r)
    db.session.add(u)
    db.session.commit()

def get_user_id(email):
    u = User.query.filter_by(email=email).first()
    return u.id