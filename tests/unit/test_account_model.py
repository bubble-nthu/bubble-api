"""import pytest
import time
from datetime import datetime
from app import create_app, db
from app.models import Role, Account

class TestCaseAccountModel:
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
    
    def test_password_setter(self):
        u = Account(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = Account(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = Account(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = Account(password='cat')
        u2 = Account(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)
"""