import pytest
import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role
from ..helper import get_basic_api_headers, get_bearer_api_headers
from app.lib.auth_token import AuthToken
from flask import current_app


class TestCaseApiRegister():
    def setup_method(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_happy_register(self):
        #generate token
        username = "river1440"
        email = "river1400@gapp.nthu.edu.tw"

        registration = {
            "username": username,
            "email": email            
        }
        registration_token = AuthToken.tokenize(registration)
        registration['verification_url'] = f"{current_app.config['BUBBLE_API_URL']}/auth/register/{registration_token}"
        #send to register
        response = self.client.post(
            f'/api/v1/auth/register',
            json=json.dumps(registration)
        )

        assert response.status_code < 300


        # get account from token
        new_account = AuthToken.detokenize(registration_token)
        
        # assert token
        assert username == new_account["username"]
        assert email == new_account["email"]

        # create new user
        data = {
            "username": new_account["username"],
            "email": new_account["email"],
            "password": "cat"
        }

        response = self.client.post(
            f'/api/v1/users',
            json=json.dumps(data)
        )
        assert response.status_code == 201
        # check if new user create

        status_code = User.query.filter_by(email=new_account["email"]).first_or_404()
        assert status_code != 404

        

    def test_happy_register_and_login(self):
        pass
        #generate token
        #sent to register
        #go to register api
        #check response code
        #login