import pytest
import time
from datetime import datetime
from app import create_app, db
from app.models import Role
from app.lib.auth_token import AuthToken


class TestCaseAuthToken:
    def setup_method(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()


    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_happy_should_detokenize_token(self):
        payload = {
          "key": "value",
           "key2": 12
        }

        token = AuthToken.create(payload)
        auth = AuthToken(token)
        assert auth.payload == payload

    def test_sad_expired_token(self):
        payload = {
          "key": "value",
           "key2": 12
        }

        token = AuthToken.create(payload, expiration = -(60*60))
        auth = AuthToken(token)
        assert auth.check_expired() == True
        assert auth.check_fresh() == False

    def test_sad_wrong_token(self):
        payload1 = {
          "key": "value",
           "key2": 12
        }

        payload2 = {
          "key": "not cool",
           "key2": 12345
        }

        token1 = AuthToken.create(payload1)
        token2 = AuthToken.create(payload2)

        auth1 = AuthToken(token1)
        auth2 = AuthToken(token2)
        assert auth1.payload == payload1
        assert auth2.payload != payload1

