import base64
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

from typing import Tuple

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryptor:
    def __init__(self):
        self._sender_public_key = None
        self._sender_private_key = None
        self._server_public_key = None

    @staticmethod
    def asymmetric_encrypt_message(message: bytes, key):
        encrypted = key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    @staticmethod
    def asymmetric_decrypt_message(enscrypted_message: bytes, key):
        original_message = key.decrypt(
            enscrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original_message

    @staticmethod
    def generate_keys(public_exponent=65537, key_size=2048, backend=default_backend) -> Tuple:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=backend()
        )
        public_key = private_key.public_key()
        return public_key, private_key

    @staticmethod
    def save_private_key(private_key, location: str = 'test_private_key.pem'):
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(location, 'wb') as f:
            f.write(pem)

    @staticmethod
    def save_public_key(public_key, location: str = 'test_public_key.pem'):
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(location, 'wb') as f:
            f.write(pem)

    @staticmethod
    def load_private_key(location: str = 'test_private_key.pem'):
        with open(location, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    @staticmethod
    def load_public_key(location: str = 'test_public_key.pem'):
        with open(location, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    #key = Fernet.generate_key()
    @staticmethod
    def symmetrical_encrypt(key: bytes, message: bytes):
        f = Fernet(key)
        return f.encrypt(message)

    @staticmethod
    def symmetrical_decrypt(key: bytes, message: bytes):
        f = Fernet(key)
        return f.decrypt(message)

    @staticmethod
    def save_symmetrical_key(key: bytes):
        file = open('key.key', 'wb')
        file.write(key)
        file.close()

    @staticmethod
    def load_symmetrical_key(key: bytes):
        file = open('key.key', 'rb')
        key = file.read(key)  # The key will be type bytes
        file.close()

    @staticmethod
    def generate_symmetrical_key_from_seed(seed: bytes):
        salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(seed))  # Can only use kdf once

    @staticmethod
    def create_signature(private_key, message: bytes) -> bytes:
        hashed_msg = hashlib.sha256(message).hexdigest().encode()
        signature = private_key.sign(
            hashed_msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())
        return signature

    @staticmethod
    def signature_is_valid(signature, public_key, message: bytes) -> bool:
        hashed_msg = hashlib.sha256(message).hexdigest().encode()
        try:
            public_key.verify(
                signature,
                hashed_msg,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256())
            return True
        except InvalidSignature:
            return False


#print(base64.b64encode(sig))
#decoded_sig = base64.b64decode(sig)


