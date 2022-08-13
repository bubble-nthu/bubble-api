from app.models import User
from app.lib.auth_token import AuthToken

class UnauthorizedError(Exception):
    def __init__(self, username = None):
      super
      self.username = username

    def message(self):
      return f"Invalid Credentials for: #{self.username}"

class AuthenticateUser:

    @classmethod
    def call(self, user):
        user = User.query.filter_by(email=user.email).first()
        user_content = {
          "username": user.username,
          "email": user.email
        }
        return AuthenticateUser.user_and_token(user_content)
    
    @classmethod
    def user_and_token(self, user_content):
        content = {
          "type": 'authenticated_user',
          "attributes": {
            "user": user_content,
            "auth_token": AuthToken.create(user_content)
          }
        }
        return content