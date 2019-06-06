import json

from user_message import UserMessage
from typing import List


class Dialog:
    def __init__(self, messages: List[UserMessage] = None):
        if messages is None:
            self.messages = []
        else:
            self.messages: List[UserMessage] = messages

    def add_message(self, message: UserMessage):
        self.messages.append(message)

    def get_messages(self) -> List[UserMessage]:
        return self.messages

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    @classmethod
    def from_json(cls, arg):
        return Dialog(messages=list(map(UserMessage.from_json, arg["messages"])))