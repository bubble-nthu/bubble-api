import pytest
import time
from datetime import datetime
from app import create_app, db
from app.models import Role, User

class TestCaseProfile:
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

    def test_timestamps(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - u.profile.member_since).total_seconds() < 3)
        self.assertTrue(
            (datetime.utcnow() - u.profile.last_seen).total_seconds() < 3)

    def test_ping(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.profile.last_seen
        u.profile.ping()
        self.assertTrue(u.profile.last_seen > last_seen_before)

    def test_gravatar(self):
        u = User(email='john@example.com', password='cat')
        with self.app.test_request_context('/'):
            gravatar = u.profile.gravatar()
            gravatar_256 = u.profile.gravatar(size=256)
            gravatar_pg = u.profile.gravatar(rating='pg')
            gravatar_retro = u.profile.gravatar(default='retro')
        self.assertTrue('https://secure.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'in gravatar)
        self.assertTrue('s=256' in gravatar_256)
        self.assertTrue('r=pg' in gravatar_pg)
        self.assertTrue('d=retro' in gravatar_retro)