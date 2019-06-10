import json
from typing import List, Dict

from encrytor import Encryptor
from user_message import UserMessage


class User:
    def __init__(self, username, password, email: str = '',
                 undelivered_messages: List[UserMessage] = None):
        self.username: str = username
        self.password: str = password
        self.email: str = email
        if undelivered_messages is None:
            self.undelivered_messages: List[UserMessage] = []
        else:
            self.undelivered_messages = undelivered_messages

    def get_username(self):
        return self.username

    def check_password(self, password: str) -> bool:
        password = Encryptor.hash_message(password.encode())
        password = password.decode()
        return password == self.password

    def add_undelivered_message(self, message: UserMessage):
        if isinstance(message, UserMessage):
            self.undelivered_messages.append(message)
        else:
            raise TypeError

    def get_undelivered_messages(self) -> List[UserMessage]:
        return self.undelivered_messages

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    @classmethod
    def from_json(cls, arg):
        return User(username=arg['username'], password=arg['password'], email=arg['email'],
                    undelivered_messages=list(map(UserMessage.from_json, arg["undelivered_messages"])))


# singleton
class UsersToPublicKeys:
    class __UsersToPublicKeys:
        def __init__(self):
            self.users_to_public_keys: Dict = {}

        def __repr__(self):
            res = {}
            for k ,v in self.users_to_public_keys.items():
                res[k] = Encryptor.get_public_key_as_string(v)
            return json.dumps(res, indent=3)

    _instance: __UsersToPublicKeys = None

    def __init__(self):
        UsersToPublicKeys._instance = UsersToPublicKeys.__UsersToPublicKeys()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__UsersToPublicKeys()
        return cls._instance

    @classmethod
    def serialize(cls, path: str = 'users_to_public_keys.txt'):
        res = {}
        for k, v in cls.get_instance().users_to_public_keys.items():
            res[k] = Encryptor.get_public_key_as_string(v)
        with open(path, 'wb') as f:
            f.write(json.dumps(res).encode())

    @classmethod
    def deserialize(cls, path: str = 'users_to_public_keys.txt'):
        try:
            res = {}
            with open(path, 'rb') as f:
                file_content = f.read()
                if file_content != b'':
                    res = json.loads(file_content)
                    for k, v in res.items():
                        cls.get_instance().users_to_public_keys[k] = Encryptor.load_public_key_from_string(v)
        except FileNotFoundError:
            print('No such file')

    @classmethod
    def add_user_public_key(cls, username: str, public_key):
        if isinstance(public_key, str):
            public_key = Encryptor.load_public_key_from_string(public_key)
        cls.get_instance().users_to_public_keys[username] = public_key

    @classmethod
    def get_public_key(cls, username: str):
        return UsersToPublicKeys.get_instance().users_to_public_keys[username]

# singleton
class Users:
    class __Users:
        def __init__(self, users: List[User] = None):
            if users is None:
                self.users = []
            else:
                self.users = users

        def __repr__(self):
            return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    _instance: __Users = None

    def __init__(self, users: List[User] = None):
        Users._instance = Users.__Users(users)

    @classmethod
    def from_json(cls, arg):
        return Users(users=list(map(User.from_json, arg["users"])))

    @classmethod
    def serialize(cls, path: str = 'users.txt'):
        with open(path, 'w') as f:
            f.write(str(cls.get_instance()))
        UsersToPublicKeys.serialize()

    @classmethod
    def deserialize(cls, path: str = 'users.txt'):
        try:
            with open(path, 'r') as f:
                file_content = f.read()
                if file_content != '':
                    Users.from_json(json.loads(file_content))
            UsersToPublicKeys.deserialize()
        except FileNotFoundError:
            cls._instance = cls.__Users()
        finally:
            print(Users.get_instance())
            print(UsersToPublicKeys.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__Users()
        return cls._instance

    @classmethod
    def get_users(cls):
        return cls.get_instance().users

    @classmethod
    def get_user(cls, username: str):
        for usr in cls.get_instance().users:
            if usr.username == username:
                return usr
        raise KeyError

    @classmethod
    def add_user(cls, user: User):
        if isinstance(user, User):
            cls.get_instance().users.append(user)
        else:
            raise TypeError

    @classmethod
    def user_exists(cls, username):
        return username in UsersToPublicKeys.get_instance().users_to_public_keys

    @classmethod
    def get_public_key(cls, username: str):
        return UsersToPublicKeys.get_instance().users_to_public_keys[username]
