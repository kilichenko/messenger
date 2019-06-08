import base64
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Crypto is used for generation and saving keys because of the issue with loading keys from a file
# after saving those generated with cryptography
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from typing import Tuple



class Encryptor:
    @staticmethod
    def hash_message(message: bytes) -> bytes:
        return hashlib.sha256(message).hexdigest().encode()

    @staticmethod
    def asymmetric_encrypt_message(key, message: bytes):
        #cipher = PKCS1_OAEP.new(key=key)
        #encrypted = cipher.encrypt(message)
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
    def asymmetric_decrypt_message(key, message: bytes, ):
        #decrypt = PKCS1_OAEP.new(key=key)
        #decrypt.decrypt(enscrypted_message)
        original_message = key.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original_message

    @staticmethod
    def generate_keys(key_size=2048) -> Tuple:
        private_key = RSA.generate(key_size)
        return private_key.publickey(), private_key

    @staticmethod
    def save_private_key(private_key, location: str = '', file_name: str = 'private_key'):
        private_pem = private_key.export_key().decode()
        with open(location + file_name + '.pem', 'w') as pr:
            pr.write(private_pem)

    @staticmethod
    def save_public_key(public_key, location: str = '', file_name: str = 'public_key'):
        public_pem = public_key.export_key().decode()
        with open(location + file_name + '.pem', 'w') as pr:
            pr.write(public_pem)

    @staticmethod
    def load_private_key(location: str = '', file_name: str = 'private_key'):
        # return RSA.import_key(open(location + file_name + '.pem', 'r').read())
        with open(location + file_name + '.pem', "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        return private_key

    @staticmethod
    def load_public_key(location: str = '', file_name: str = 'public_key'):
        # return RSA.import_key(open(location + file_name + '.pem', 'r').read())
        with open(location + file_name + '.pem', "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        return public_key

    @staticmethod
    def load_public_key_as_bytes(location: str = '', file_name: str = 'public_key') -> bytes:
        with open(location + file_name + '.pem', "rb") as key_file:
            return key_file.read()

    @staticmethod
    def generate_symmetric_key():
        return Fernet.generate_key()

    @staticmethod
    def symmetrical_encrypt(key: bytes, message: bytes):
        f = Fernet(key)
        return f.encrypt(message)

    @staticmethod
    def symmetrical_decrypt(key: bytes, message: bytes):
        f = Fernet(key)
        return f.decrypt(message)

    @staticmethod
    def save_symmetrical_key(key: bytes, location: str = '', file_name: str = 'symmetric_key'):
        with open(location + file_name + '.key', 'wb') as f:
            f.write(key)

    @staticmethod
    def load_symmetrical_key(location: str = '', file_name: str = 'symmetric_key'):
        with open(location + file_name + 'key', 'rb') as f:
            return f.read()  # The key will be type bytes

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
        return base64.urlsafe_b64encode(kdf.derive(seed))  # Can only use kdf once

    @staticmethod
    def get_next_symmetrical_key(key: bytes):
        return Encryptor.generate_symmetrical_key_from_seed(Encryptor.hash_message(key))

    @staticmethod
    def create_signature(private_key, message: bytes) -> bytes:
        hashed_msg = Encryptor.hash_message(message)
        signature = private_key.sign(
            hashed_msg,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256())
        return signature

    @staticmethod
    def signature_is_valid(signature, public_key, message: bytes) -> bool:
        hashed_msg = Encryptor.hash_message(message)
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


#pubk1, prkey1 = Encryptor.generate_keys()
#print(type(pubk1))
#pubk2 = Encryptor.load_public_key(file_name='gleb_public_key')
#prk2 = Encryptor.load_private_key(file_name='gleb_private_key')
#print(type(pubk2))