import nacl.secret
import nacl.utils
from base64 import urlsafe_b64decode, urlsafe_b64encode

def generate_secret_key(key_size=nacl.secret.SecretBox.KEY_SIZE):
    """
    returns a base64 encoded string of raw bytes
    """

    try:
        key = urlsafe_b64encode(nacl.utils.random(key_size)).decode()
        return key
    except:
        raise

def decode_secret_key(key_string):
    """
    takes a base64 encoded string and decodes the return to raw bytes
    """
    try:
        key = urlsafe_b64decode(key_string)
        assert(type(key) is bytes)
        assert(len(key) == nacl.secret.SecretBox.KEY_SIZE)
        return key
    except:
        raise

def create_secret_box(key):
    try:
        assert(type(key) is bytes)
        assert(len(key) == 32)
        box = nacl.secret.SecretBox(key)
        return box
    except:
        raise

def encrypt_data_with_box(box, data):
    try:
        encrypted = box.encrypt(data)
        return encrypted
    except:
        raise


