from user_message import UserMessage
from typing import List


class Dialog:
    def __init__(self):
        self.messages: List[UserMessage] = []

    def add_message(self, message: UserMessage):
        self.messages.append(message)

    def get_messages(self) -> List[UserMessage]:
        return self.messages
