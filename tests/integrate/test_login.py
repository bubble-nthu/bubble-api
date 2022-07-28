import pytest
import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role


class TestCaseApiLogin():
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

    def get_basic_api_headers(self, email, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (email + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_bearer_api_headers(self, token):
        return {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        } 

    def add_user(self, email, password, confirmed=True, role="User"):
        # add a user
        r = Role.query.filter_by(name=role).first()
        u = User(email=email, password=password, confirmed=confirmed,
                 role=r)
        db.session.add(u)
        db.session.commit()

    def get_user_id(self, email):
        u = User.query.filter_by(email=email).first()
        return u.id

    def get_token(self, email, password):
        response = self.client.post(
            '/api/v1/tokens',
            headers=self.get_basic_api_headers(email, password))

        json_response = json.loads(response.get_data(as_text=True))
        token = json_response['token']

        return token

    def test_happy_get_token(self):
        #add a user
        email = 'john@example.com'
        password = 'dog'
        wrong_password = 'cat'

        self.add_user(email, password)

        # get token 
        token = self.get_token(email, password)

        assert token != ''

    def test_sad_bad_token(self):
        #add a user
        email = 'john@example.com'
        password = 'dog'
        wrong_password = 'cat'

        self.add_user(email, password)

        # get token with bad password
        response = self.client.get(
            '/api/v1/tokens',
            headers=self.get_basic_api_headers(email, wrong_password))
        # email and password not pair, method not allow
        assert response.status_code == 405

    def test_happy_login(self):
        email = 'john@example.com'
        password = 'dog'

        self.add_user(email, password)
        token = self.get_token(email, password)

        id = self.get_user_id(email)

        # issue a request with the token
        response = self.client.get(
            f'/api/v1/users/{id}',
            headers=self.get_bearer_api_headers(token))
        assert response.status_code == 200

    def test_sad_404(self):
        response = self.client.get(
            '/api/v1/wrong/url',
            headers=self.get_basic_api_headers('email', 'password'))
        assert response.status_code == 404

        # test error message
        """json_response = json.loads(response.get_data(as_text=True))
        assert json_response['error'] == 'not found'"""

    def test_sad_no_auth(self):
        response = self.client.get('/api/v1/users/1',
                                   content_type='application/json')
        assert response.status_code == 401

    def test_sad_anonymous_no_token(self):
        response = self.client.get(
            '/api/v1/tokens',
            headers=self.get_basic_api_headers('', ''))
        
        # no email and password, method not fit
        assert response.status_code == 405

    def test_sad_unconfirmed_account_get_403(self):
        # add an unconfirmed user
        email = 'john@example.com'
        password = 'cat'
        self.add_user(email = email, password = password, confirmed=False)

        # can not get toke
        response = self.client.get(
            '/api/v1/tokens',
            headers=self.get_basic_api_headers(email, password))
        # email and password not pair, method not allow
        assert response.status_code == 405
        