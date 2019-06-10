from encryptor import Encryptor
from request import Request
from typing import Dict


# singleton
class ClientSession:
    class __ClientSession:
        def __init__(self, username: str, password: str):
            self.username: str = username
            self.client_private_key = Encryptor.load_private_key(file_name=self.username + '_private_key')
            self.client_public_key = Encryptor.load_public_key(file_name=self.username + '_public_key')
            self.server_public_key = Encryptor.load_public_key()
            self.server_symmetric_key = None
            self.server_pub_k = Encryptor.load_public_key()
            self.password = Encryptor.asymmetric_encrypt_message(key=self.server_pub_k, message=password)
            self.recipients_symmetric_keys: Dict = {} #probably should be in ContactsToSymmetricKeys
            #self.recipients_public_keys: Dict = {}

    _instance: __ClientSession = None

    def __init__(self, username, password):
        ClientSession._instance = ClientSession.__ClientSession(username, password)

    @classmethod
    def get_instance(cls):
        return cls._instance

    @classmethod
    def get_username(cls):
        return cls._instance.username

    @classmethod
    def establish_session(cls):
        request = Request(action='authenticate',
                          request_content={'username': cls.get_instance().username,
                                           'password': cls.get_instance().password},
                          request_sender=cls.get_instance().username)
        request.send_request()

    @classmethod
    def get_client_public_key(cls):
        return cls.get_instance().client_public_key

    @classmethod
    def get_client_private_key(cls):
        return cls.get_instance().client_private_key

    @classmethod
    def set_server_symmetric_key(cls, symmetric_key):
        cls.get_instance().server_symmetric_key = Encryptor.asymmetric_decrypt_message(
            key=cls.get_instance().client_private_key, message=symmetric_key)
        print(cls.get_instance().server_symmetric_key)

    @classmethod
    def get_server_symmetric_key(cls):
        return cls._instance.server_symmetric_key

    @classmethod
    def add_recipient_symmetric_key(cls, username: str, key):
        key = Encryptor.asymmetric_decrypt_message(key=cls.get_instance().client_private_key, message=key)
        cls.get_instance().recipients_symmetric_keys[username] = key
        print('decrypted symmetric key added for ', username, ': ', key)

    @classmethod
    def get_recipient_symmetric_key(cls, username: str):
        return cls.get_instance().recipients_symmetric_keys[username]

    #@classmethod
    #def add_recipient_public_key(cls, username, key):
    #    cls.get_instance().recipients_public_keys[username] = key

    #@classmethod
    #def get_recipient_public_key(cls, username: str):
    #    return cls.get_instance().recipients_public_keys[username]
