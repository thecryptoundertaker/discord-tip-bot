import nacl.secret
import nacl.utils
from nacl.encoding import URLSafeBase64Encoder
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
        box = nacl.secret.SecretBox(key, encoder=URLSafeBase64Encoder)
        return box
    except:
        raise

def encrypt_data_in_box(box, data):
    try:
        encrypted = box.encrypt(data, encoder=URLSafeBase64Encoder)
        return encrypted
    except:
        raise


def decrypt_data_in_box(box, data):
    try:
        decrypted = box.decrypt(data, encoder=URLSafeBase64Encoder)
        return decrypted
    except:
        raise
