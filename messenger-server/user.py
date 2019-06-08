import json
from typing import List, Dict

from encrytor import Encryptor
from user_message import UserMessage
from dialog import Dialog


class User:
    def __init__(self, username, password, public_key, email: str = '',
                 undelivered_messages: List[UserMessage] = None, dialogs: Dict[str, Dialog] = None):
        self.username: str = username
        self.password: str = Encryptor.hash_message(password.encode()).decode()
        self.email: str = email
        self.public_key = public_key
        if undelivered_messages is None:
            self.undelivered_messages: List[UserMessage] = []
        else:
            self.undelivered_messages = undelivered_messages
        if dialogs is None:
            self.dialogs: Dict[str, Dialog] = {}
        else:
            self.dialogs = dialogs
        # Users.add_user(self)

    def get_username(self):
        return self.username

    def get_public_key(self):
        return self.public_key

    def check_password(self, password: str) -> bool:
        return Encryptor.hash_message(password.encode()) == self.password.encode()

    def add_undelivered_message(self, message: UserMessage):
        if isinstance(message, UserMessage):
            self.undelivered_messages.append(message)
        else:
            raise TypeError

    def get_undelivered_messages(self) -> List[UserMessage]:
        return self.undelivered_messages

    def get_dialog_with(self, username: str) -> Dialog:
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

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    @classmethod
    def from_json(cls, arg):
        dialogs = {}
        for k, v in arg['dialogs'].items():
            dialogs[k] = Dialog(messages=list(map(UserMessage.from_json, v["messages"])))
        return User(username=arg['username'], password=arg['password'], public_key=arg['public_key'],
                    email=arg['email'],
                    undelivered_messages=list(map(UserMessage.from_json, arg["undelivered_messages"])),
                    dialogs=dialogs)


# singleton
class Users:
    _instance = None

    class __Users:
        def __init__(self, users: List[User] = None, users_to_public_keys: Dict = None):
            if users is None:
                self.users = []
            else:
                self.users = users
            if users_to_public_keys is None:
                self.users_to_public_keys = {}
            else:
                self.users_to_public_keys = users_to_public_keys

        def __repr__(self):
            return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    def __init__(self, users: List[User] = None, users_to_public_keys: Dict = None):
        Users._instance = Users.__Users(users, users_to_public_keys)

    @classmethod
    def from_json(cls, arg):
        return Users(users=list(map(User.from_json, arg["users"])), users_to_public_keys=arg['users_to_public_keys'])

    @classmethod
    def serialize(cls, path: str = 'users.txt'):
        with open(path, 'w') as f:
            f.write(str(cls.get_instance()))

    @classmethod
    def deserialize(cls, path: str = 'users.txt'):
        try:
            with open(path, 'r') as f:
                file_content = f.read()
                if file_content != '':
                    Users.from_json(json.loads(file_content))
        except FileNotFoundError:
            cls._instance = cls.__Users()
        finally:
            print(Users.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__Users()
        return cls._instance

    @classmethod
    def get_users(cls):
        return cls._instance.users

    @classmethod
    def get_user(cls, username: str):
        for usr in cls._instance.users:
            if usr.username == username:
                return usr
        raise KeyError

    @classmethod
    def add_user(cls, user: User):
        if isinstance(user, User):
            cls._instance.users.append(user)
            cls._instance.users_to_public_keys[user.username] = user.public_key
        else:
            raise TypeError

    @classmethod
    def user_exists(cls, username):
        return username in cls._instance.users_to_public_keys

    @classmethod
    def get_public_key(cls, username: str):
        return cls._instance.users_to_public_keys[username]
