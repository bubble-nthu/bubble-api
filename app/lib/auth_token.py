# frozen_string_literal: true

import base64
from datetime import datetime, timedelta
import json

from .securable import SecureMixin

## Token and Detokenize Authorization Information
# Usage examples:
#  AuthToken.setup(AuthToken.generate_key)
#  token = AuthToken.create({ key: 'value', key2: 12 }, AuthToken::ONE_MONTH)
#  AuthToken.new(token).payload   # => {"key"=>"value", "key2"=>12}

class ExpiredTokenError(Exception):
    pass
class InvalidTokenError(Exception):
    pass

class AuthToken(SecureMixin):

    # Extract information from a token
    def __init__(self, token):
        self.token = token
        contents = self.detokenize(self.token)
        self.expiration = contents['exp']
        self.payload = contents['payload']

    ONE_HOUR = 60 * 60
    ONE_DAY = ONE_HOUR * 24
    ONE_WEEK = ONE_DAY * 7
    ONE_MONTH = ONE_WEEK * 4
    ONE_YEAR = ONE_MONTH * 12

    # Check if token is expired
    def check_expired(self):
        now = datetime.utcnow()
        if self.exp_to_time() > now + timedelta(seconds=60):
            raise InvalidTokenError

        return self.exp_to_time() < (now + timedelta(seconds=60))


    # Check if token is not expired
    def check_fresh(self):
        return not self.check_expired()

    # Extract data from token
    def payload(self):
      raise(ExpiredTokenError) if self.expired else self.payload

    def get_token(self):
        return self.token

    def exp_to_time(self):
        return datetime.fromtimestamp(self.expiration)

    # Create a token from a Hash payload
    @classmethod
    def create(self, payload, expiration = ONE_WEEK):
        content = {
          'payload': payload,
          'exp': AuthToken.expires(expiration)
        }
        return AuthToken.tokenize(content)

    # Tokenize contents or return nil if no data
    @classmethod
    def tokenize(self, message):
        if not message:
            return ""

        message_json = json.dumps(message)
        ciphertext = SecureMixin.base_encrypt(self, message_json)
        return base64.urlsafe_b64encode(ciphertext).decode('utf-8')

    # Detokenize and return contents, or raise error
    @classmethod
    def detokenize(self, ciphertext64):
        if not ciphertext64:
            return ""

        ciphertext = base64.urlsafe_b64decode(ciphertext64.encode('utf-8'))
        message_json = SecureMixin.base_decrypt(self, ciphertext)
        return json.loads(message_json)

    @classmethod
    def expires(self, expiration):
      return int(datetime.utcnow().timestamp() + expiration)