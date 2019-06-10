import json
from typing import List, Dict

from encryptor import Encryptor
from user_message import UserMessage


class Contact:
    def __init__(self, username, messages: List[UserMessage] = None):
        self.username: str = username
        if messages is None:
            self.messages: List[UserMessage] = []
            pass
        else:
            self.messages = messages
            pass

    def add_message(self, message: UserMessage):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def get_username(self):
        return self.username

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    @classmethod
    def from_json(cls, arg):
        return Contact(username=arg['username'],
                       messages=list(map(UserMessage.from_json, arg["messages"])))


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
    def serialize(cls, username, path: str = '_contacts_to_public_keys.txt'):
        res = {}
        for k, v in cls.get_instance().contacts_to_public_keys.items():
            res[k] = Encryptor.get_public_key_as_string(v)
        with open(username + path, 'wb') as f:
            f.write(json.dumps(res).encode())

    @classmethod
    def deserialize(cls, username, path: str = '_contacts_to_public_keys.txt'):
        try:
            res = {}
            with open(username + path, 'rb') as f:
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
        def __init__(self, contacts: List[Contact] = None, pending_connects: List[Contact] = None):
            if contacts is None:
                self.contacts = []
            else:
                self.contacts = contacts
            if pending_connects is None:
                self.pending_connects = []
            else:
                self.pending_connects = pending_connects

        def __repr__(self):
            return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    _instance: __Contacts = None

    def __init__(self, contacts: List[Contact] = None, pending_connects: List[Dict] = None):
        Contacts._instance = Contacts.__Contacts(contacts, pending_connects)

    @classmethod
    def from_json(cls, arg):
        return Contacts(contacts=list(map(Contact.from_json, arg["contacts"])),
                        pending_connects=list(map(lambda o: o, arg["pending_connects"])))

    @classmethod
    def serialize(cls, username, path: str = '_contacts.txt'):
        with open(username + path, 'w') as f:
            f.write(str(cls.get_instance()))
        ContactsToPublicKeys.serialize(username)

    @classmethod
    def deserialize(cls, username, path: str = '_contacts.txt'):
        try:
            with open(username + path, 'r') as f:
                file_content = f.read()
                if file_content != '':
                    Contacts.from_json(json.loads(file_content))
            ContactsToPublicKeys.deserialize(username)
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
    def get_contacts(cls):
        return cls.get_instance().contacts

    @classmethod
    def get_contact(cls, username: str):
        for usr in cls.get_instance().contacts:
            if usr.username == username:
                return usr
        raise KeyError

    @classmethod
    def add_contact(cls, contact: Contact):
        if isinstance(contact, Contact):
            cls.get_instance().contacts.append(contact)
        else:
            raise TypeError

    @classmethod
    def contact_exists(cls, username):
        return username in ContactsToPublicKeys.get_instance().contacts_to_public_keys

    @classmethod
    def get_public_key(cls, username: str):
        return ContactsToPublicKeys.get_instance().contacts_to_public_keys[username]

    @classmethod
    def add_pending_connect(cls, contact: Contact):
        cls.get_instance().pending_connects.append(contact)

    @classmethod
    def get_pending_connects(cls):
        return cls.get_instance().pending_connects

    @classmethod
    def pending_connect_exists(cls, username):
        return username in Contacts.get_instance().pending_connects

    @classmethod
    def remove_pending_connect(cls, username: str):
        for index, usr in enumerate(cls.get_instance().pending_connects):
            if usr.username == username:
                return cls.get_instance().pending_connects.pop(index)
