import nacl.secret
import nacl.utils
from base64 import urlsafe_b64encode

def generate_secret_key(key_size=nacl.secret.SecretBox.KEY_SIZE):
    """
    returns a base64 encoded string of raw bytes
    """

    try:
        key = urlsafe_b64encode(nacl.utils.random(key_size)).decode()
        return key
    except:
        raise

print(generate_secret_key())
