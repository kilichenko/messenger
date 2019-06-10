import json
from typing import List, Dict

from encryptor import Encryptor
import client_session
from user_message import UserMessage


class Contact:
    def __init__(self, username):
        self.username: str = username

    def get_username(self):
        return self.username

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    @classmethod
    def from_json(cls, arg):
        return Contact(username=arg['username'])


# singleton
class ContactsToPublicKeys:
    class __ContactsToPublicKeys:
        def __init__(self):
            self.contacts_to_public_keys: Dict = {}

        def __repr__(self):
            res = {}
            for k, v in self.contacts_to_public_keys.items():
                res[k] = Encryptor.get_public_key_as_string(v)
            return json.dumps(res, indent=3)

    _instance: __ContactsToPublicKeys = None

    def __init__(self):
        ContactsToPublicKeys._instance = ContactsToPublicKeys.__ContactsToPublicKeys()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__ContactsToPublicKeys()
        return cls._instance

    @classmethod
    def serialize(cls, path: str = client_session.ClientSession.get_username() + 'contacts_to_public_keys.txt'):
        res = {}
        for k, v in cls.get_instance().contacts_to_public_keys.items():
            res[k] = Encryptor.get_public_key_as_string(v)
        with open(path, 'wb') as f:
            f.write(json.dumps(res).encode())

    @classmethod
    def deserialize(cls, path: str = client_session.ClientSession.get_username() + 'contacts_to_public_keys.txt'):
        try:
            res = {}
            with open(path, 'rb') as f:
                file_content = f.read()
                if file_content != b'':
                    res = json.loads(file_content)
                    for k, v in res.items():
                        cls.get_instance().contacts_to_public_keys[k] = Encryptor.load_public_key_from_string(v)
        except FileNotFoundError:
            print('No such file')

    @classmethod
    def add_contact_public_key(cls, username: str, public_key):
        if isinstance(public_key, str):
            public_key = Encryptor.load_public_key_from_string(public_key)
        cls.get_instance().contacts_to_public_keys[username] = public_key

    @classmethod
    def get_contact_public_key(cls, username: str):
        return ContactsToPublicKeys.get_instance().contacts_to_public_keys[username]


# singleton
class Contacts:
    class __Contacts:
        def __init__(self, contacts: List[Contact] = None):
            if contacts is None:
                self.contacts = []
            else:
                self.contacts = contacts

        def __repr__(self):
            return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    _instance: __Contacts = None

    def __init__(self, contacts: List[Contact] = None, ):
        Contacts._instance = Contacts.__Contacts(contacts)

    @classmethod
    def from_json(cls, arg):
        return Contacts(contacts=list(map(Contact.from_json, arg["contacts"])))

    @classmethod
    def serialize(cls, path: str = client_session.ClientSession.get_username() + 'contacts.txt'):
        with open(path, 'w') as f:
            f.write(str(cls.get_instance()))
        ContactsToPublicKeys.serialize()

    @classmethod
    def deserialize(cls, path: str = client_session.ClientSession.get_username() + 'contacts.txt'):
        try:
            with open(path, 'r') as f:
                file_content = f.read()
                if file_content != '':
                    Contacts.from_json(json.loads(file_content))
            ContactsToPublicKeys.deserialize()
        except FileNotFoundError:
            cls._instance = cls.__Contacts()
        finally:
            print(Contacts.get_instance())
            print(ContactsToPublicKeys.get_instance())

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__Contacts()
        return cls._instance

    @classmethod
    def get_users(cls):
        return cls.get_instance().contacts

    @classmethod
    def get_user(cls, username: str):
        for usr in cls.get_instance().contacts:
            if usr.username == username:
                return usr
        raise KeyError

    @classmethod
    def add_user(cls, user: Contact):
        if isinstance(user, Contact):
            cls.get_instance().contacts.append(user)
        else:
            raise TypeError

    @classmethod
    def user_exists(cls, username):
        return username in ContactsToPublicKeys.get_instance().contacts_to_public_keys

    @classmethod
    def get_public_key(cls, username: str):
        return ContactsToPublicKeys.get_instance().contacts_to_public_keys[username]
