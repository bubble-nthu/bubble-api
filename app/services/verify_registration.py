from itsdangerous import URLSafeTimedSerializer
from flask import current_app

class VerifyRegistration:
  
    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
        return token

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email