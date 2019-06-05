import datetime
from typing import Dict
import time


class UserMessage:
    def __init__(self, sender, recipient, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.timestamp = None

    def set_timestamp(self):
        self.timestamp = time.time()

    def get_timestamp(self):
        return self.timestamp

    def get_formatted_timestamp(self):
        if self.timestamp:
            return datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y:%m:%d %H:%M:%S')

    def as_dict(self):
        return {'sender': self.sender, 'recipient': self.recipient, 'content': self.content}

    @staticmethod
    def parse_from_dict(message: Dict):
        try:
            msg = UserMessage(message['sender'], message['recipient'], message['content'])
            return msg
        except KeyError:
            return None