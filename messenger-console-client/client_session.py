from encryptor import Encryptor


class ClientSession:
    def __init__(self):
        self.client_private_key = Encryptor.load_private_key()
        self.client_public_key = Encryptor.load_public_key()
        self.server_public_key = Encryptor.load_public_key('server_public_key')
        self.symmetric_key = None

    def establish_session(self):
        #get encrypted symmetric key to the server
        pass
