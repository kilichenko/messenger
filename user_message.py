#from user import User as Usr
from typing import Dict


class UserMessage:
    def __init__(self, sender, recipient, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def asdict(self):
        return {'sender': self.sender, 'recipient': self.recipient, 'content': self.content}

    @staticmethod
    def parse_from_dict(message: Dict):
        try:
            msg = UserMessage(message['sender'], message['recipient'], message['content'])
            return msg
        except KeyError:
            return None