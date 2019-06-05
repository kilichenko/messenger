from typing import List, Dict

import u2kht
from user_message import UserMessage
from dialog import Dialog


class User:
    def __init__(self, username, password, public_key: str):
        self.username: str = username
        self.password: str = password
        self.pKey: str = public_key
        self.undelivered_messages: List[UserMessage] = []
        self.dialogs: Dict[str, Dialog] = {}
        u2kht.add_user(self)
        Users.users.append(self)

    def add_undelivered_message(self, message: UserMessage):
        if isinstance(message, UserMessage):
            self.undelivered_messages.append(message)
        else:
            raise TypeError

    def get_undelivered_messages(self) -> List[UserMessage]:
        return self.undelivered_messages

    def get_dialog_with(self, username: str) -> Dict:
        dialog = self.dialogs.get(username)
        if dialog is None:
            raise KeyError
        return dialog

    def get_all_dialogs(self) -> Dict[str, Dialog]:
        return self.dialogs

    def add_msg_to_dialog(self, username: str, msg: UserMessage):
        dialog = self.dialogs.get(username)
        if dialog is not None:
            dialog.add_message(msg)
        else:
            dialog = self.dialogs[username] = Dialog()
            dialog.add_message(msg)


class Users:
    users: List[User] = []

    @classmethod
    def get_user(cls, username: str):
        for usr in cls.users:
            if usr.username == username:
                return usr
        raise KeyError

    @classmethod
    def add_user(cls, user: User):
        if isinstance(user, User):
            cls.users.append(user)
        else:
            raise TypeError
