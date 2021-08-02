from loguru import logger
import nacl.secret
import nacl.utils
from nacl.encoding import URLSafeBase64Encoder
from base64 import urlsafe_b64decode, urlsafe_b64encode
from config import config

@logger.catch(level="CRITICAL")
def create_secret_box(key):
    try:
        box = nacl.secret.SecretBox(key, encoder=URLSafeBase64Encoder)
        return box
    except:
        raise

@logger.catch(level="CRITICAL")
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


@logger.catch(level="CRITICAL")
def decrypt_data(data, box=None):
    try:
        if not box:
            box = create_secret_box(config["SECRET_KEY"])
        decrypted = box.decrypt(data, encoder=URLSafeBase64Encoder)
        return decrypted.decode('utf-8')
    except:
        raise
