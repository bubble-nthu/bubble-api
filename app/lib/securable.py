import base64
import nacl.secret
import nacl.utils

class SecureMixin():
    # Generate key for Rake tasks (typically not called at runtime)
    def generate_key(self):
        # This must be kept secret, this is the combination to your safe
        self.key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        return base64.b64encode(self.key)

    # Call setup once to pass in config variable with MSG_KEY attribute
    @classmethod
    def setup(self, base_key):
        self.base_key = base_key
        self.key = base64.b64decode(self.base_key)
  

    # Encrypt with no checks
    def base_encrypt(self, plaintext):
        box = nacl.secret.SecretBox(self.key)
        return box.encrypt(plaintext.encode('utf-8'))

    # Decrypt with no checks
    def base_decrypt(self, ciphertext):
        box = nacl.secret.SecretBox(self.key)
        return box.decrypt(ciphertext).decode('utf-8')
