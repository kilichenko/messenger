#from user import User as Usr

class UserMessage:
    def __init__(self, sender, recipient, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def asdict(self):
        return {'sender': self.sender, 'recipient': self.recipient, 'content': self.content}