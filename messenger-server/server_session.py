from encrytor import Encryptor
from typing import Dict


# singleton
class ServerSession:
    class __ServerSession:
        def __init__(self):
            self.server_private_key = Encryptor.load_private_key()
            self.server_public_key = Encryptor.load_public_key()
            self.clients_to_session_keys: Dict[str, bytes] = {}

    _instance: __ServerSession = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__ServerSession()
        return cls._instance

    @classmethod
    def add_client_session_key(cls, username: str, key):
        cls.get_instance().clients_to_session_keys[username] = key

    @classmethod
    def get_client_session_key(cls, username: str):
        return cls.get_instance().clients_to_session_keys[username]

    @classmethod
    def get_private_key(cls):
        return cls.get_instance().server_private_key

    @classmethod
    def get_public_key(cls):
        return cls.get_instance().server_public_key