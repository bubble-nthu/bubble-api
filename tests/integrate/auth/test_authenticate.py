import pytest
import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role
from app.lib.auth_token import AuthToken
from app.controller.auth import NoTokenError
from ..helper import get_basic_api_headers, get_bearer_api_headers, add_user, get_user_id


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
 

    def get_auth_user(self, email, password):

        response = self.client.post(
            '/api/v1/auth/authenticate',
            headers=get_basic_api_headers(email, password))

        json_response = json.loads(response.get_data(as_text=True))
        auth_user = json_response['data']

        return auth_user

    def test_happy_get_token(self):
        #add a user
        email = 'john@example.com'
        username = 'john'
        password = 'dog'

        add_user(email, password, username)

        auth_user = self.get_auth_user(email, password)
        auth = AuthToken(auth_user["attributes"]["auth_token"])

        assert auth.payload['email'] == email
        assert auth.payload['username'] == username
        with pytest.raises(KeyError):
            auth.payload['password']
        with pytest.raises(KeyError):
            auth.payload['id']


    def test_sad_bad_token(self):
        #add a user
        email = 'john@example.com'
        password = 'dog'
        username = 'john'
        wrong_password = 'cat'

        add_user(email, password, username)

        # get token with bad password
        response = self.client.get(
            '/api/v1/auth/authenticate',
            headers=get_basic_api_headers(email, wrong_password))
        # email and password not pair, method not allow
        assert response.status_code == 405

    def test_happy_login(self):
        email = 'john@example.com'
        password = 'dog'
        username = 'john'

        add_user(email, password, username)
        auth_user = self.get_auth_user(email, password)
        auth = AuthToken(auth_user["attributes"]["auth_token"])
        auth_token = auth.get_token()

        id = get_user_id(email)

        # issue a request with the token
        response = self.client.get(
            f'/api/v1/users/{id}',
            headers=get_bearer_api_headers(auth_token))
        assert response.status_code == 200

    def test_sad_404(self):
        response = self.client.get(
            '/api/v1/wrong/url',
            headers=get_basic_api_headers('email', 'password'))
        assert response.status_code == 404

        # test error message
        """json_response = json.loads(response.get_data(as_text=True))
        assert json_response['error'] == 'not found'"""

    def test_sad_no_auth(self):
        #since no token, the request will get 401 UNAUTHORIZED
        response = self.client.get('/api/v1/users/1',
                                   content_type='application/json')
        assert response.status_code == 401                           

    def test_sad_anonymous_no_token(self):
        response = self.client.get(
            '/api/v1/auth/authenticate',
            headers=get_basic_api_headers('', ''))
        
        # no email and password, method not fit
        assert response.status_code == 405

    def test_sad_unconfirmed_account_get_403(self):
        # add an unconfirmed user
        email = 'john@example.com'
        password = 'cat'
        username = 'username'
        add_user(email = email, password = password, username=username, confirmed=False)

        # can not get toke
        response = self.client.get(
            '/api/v1/auth/authenticate',
            headers=get_basic_api_headers(email, password))
        # email and password not pair, method not allow
        assert response.status_code == 405
        