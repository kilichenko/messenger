from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Enscryptor:
    def __init__(self):
        self._sender_public_key = None
        self._sender_private_key = None
        self._server_public_key = None

    @staticmethod
    def simple_encrypt_message(message: str, key):
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
    def simple_descrypt_message(enscrypted_message: str, key):
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
    def generate_keys(public_exponent=65537, key_size=2048, backend=default_backend):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
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


# pub_k, pr_k = generate_keys()
message = b'encrypt me!'
# message = encrypt_message(message, pub_k)
print(message)
# message = descrypt_message(message, pr_k)
print(message)
