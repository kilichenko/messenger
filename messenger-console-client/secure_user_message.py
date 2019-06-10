from client_session import ClientSession
from encryptor import Encryptor
from user_message import UserMessage


class SecureUserMessage(UserMessage):
    def __init__(self, sender: str, recipient: str, content: str, timestamp=None):
        self.signature = Encryptor.create_signature(private_key=ClientSession.get_client_private_key(),
                                                    message=content.encode())
        recipient_encrypted_content = Encryptor.symmetrical_encrypt(
            key=ClientSession.get_recipient_symmetric_key(recipient),
            message=content
        )
        super(SecureUserMessage, self).__init__(sender, recipient, recipient_encrypted_content)
