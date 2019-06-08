from encryptor import Encryptor
from user_message import UserMessage


class SecureUserMessage(UserMessage):
    def __init__(self, sender: str, recipient: str, content: str,
                 sender_public_key, sender_private_key, recipient_public_key, timestamp=None):
        super(SecureUserMessage, self).__init__(sender, recipient, content)
        self.signature = Encryptor.create_signature(private_key=sender_private_key, message=content.encode())
