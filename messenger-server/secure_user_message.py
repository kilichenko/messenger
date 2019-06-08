from user_message import UserMessage


class SecureUserMessage(UserMessage):
    def __init__(self, sender: str, recipient: str, content: str, timestamp=None):
        super(SecureUserMessage, self).__init__(sender, recipient, content)
