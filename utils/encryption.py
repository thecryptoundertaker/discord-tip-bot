import nacl.secret
import nacl.utils
from nacl.encoding import URLSafeBase64Encoder
from base64 import urlsafe_b64decode, urlsafe_b64encode
from config import config

# needed only for setup
def generate_secret_key(key_size=nacl.secret.SecretBox.KEY_SIZE):
    """
    returns a base64 encoded string of raw bytes
    """

    try:
        key = urlsafe_b64encode(nacl.utils.random(key_size)).decode()
        return key
    except:
        raise

def create_secret_box(key):
    try:
        box = nacl.secret.SecretBox(key, encoder=URLSafeBase64Encoder)
        return box
    except:
        raise

def encrypt_data(data, box=None):
    try:
        if isinstance(data, str):
            data = data.encode('utf-8')
        if not box:
            box = create_secret_box(config["SECRET_KEY"])
        encrypted = box.encrypt(data, encoder=URLSafeBase64Encoder)
        return encrypted
    except:
        raise


def decrypt_data(data, box=None):
    try:
        if not box:
            box = create_secret_box(config["SECRET_KEY"])
        decrypted = box.decrypt(data, encoder=URLSafeBase64Encoder)
        return decrypted.decode('utf-8')
    except:
        raise
