import pytest
import time
from datetime import datetime
from app import create_app, db
from app.models import Role
from app.lib.securable import SecureMixin


class TestCaseLib:
    def setup_method(self):
        self.app = create_app('testing')
        SecureMixin.setup(self.app.config['MSG_KEY'])
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()


    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_happy_should_encrypt_text(self):
        text = "plaintext"
        SecureCls = SecureMixin()

        assert SecureCls.base_encrypt(text) != text

    def test_happy_should_decrypt_text(self):
        text = "plaintext"
        SecureCls = SecureMixin()
        encrypt = SecureCls.base_encrypt(text)
        decrypt = SecureCls.base_decrypt(encrypt)

        assert decrypt == text

    def test_happy_should_decrypt_non_ASCII_text(self):
        text = "泡泡飄起來！"
        SecureCls = SecureMixin()
        encrypt = SecureCls.base_encrypt(text)
        decrypt = SecureCls.base_decrypt(encrypt)

        assert decrypt == text
