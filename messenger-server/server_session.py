from encrytor import Encryptor
from typing import Dict


# singleton
class ServerSession:
    _instance = None

    class __ServerSession:
        def __init__(self):
            self.server_private_key = Encryptor.load_private_key()
            self.server_public_key = Encryptor.load_public_key()
            self.clients_to_session_keys: Dict[str, bytes] = {}

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__Users()
        return cls._instance

    @classmethod
    def add_client_session_key(self, username: str, key: bytes):
        self._instance.clients_to_session_keys[username] = key
