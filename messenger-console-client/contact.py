import json
from typing import List, Dict

from encryptor import Encryptor
from user_message import UserMessage


class Contact:
    def __init__(self, username, connected: bool = False, messages: List[UserMessage] = None):
        self.username: str = username
        self.connected: bool = connected
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

    def is_connected(self) -> bool:
        return self.connected

    def set_connected(self, connected: bool):
        self.connected = connected

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    @classmethod
    def from_json(cls, arg):
        return Contact(username=arg['username'],
                       messages=list(map(UserMessage.from_json, arg["messages"])),
                       connected=arg['connected'])


# singleton
class ContactsToKeys:
    class __ContactsToPublicKeys:
        def __init__(self):
            self.contacts_to_keys: Dict = {}

        def __repr__(self):
            res = {}
            if self.contacts_to_keys != {}:
                for k, v in self.contacts_to_keys.items():
                    res[k] = {
                        'public_key': Encryptor.get_public_key_as_string(v['public_key']),
                        'symmetric_key': v['symmetric_key']
                    }
            return json.dumps(res, indent=3)

    _instance: __ContactsToPublicKeys = None

    def __init__(self):
        ContactsToKeys._instance = ContactsToKeys.__ContactsToPublicKeys()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__ContactsToPublicKeys()
        return cls._instance

    @classmethod
    def serialize(cls, username, location: str = 'data/', file_name: str = '_contacts_to_keys'):
        res = {}

        for k, v in cls.get_instance().contacts_to_keys.items():
            try:
                res[k] = {
                    'public_key': Encryptor.get_public_key_as_string(v['public_key']),
                    'symmetric_key': v['symmetric_key']
                }
            except KeyError:
                res[k] = {
                    'public_key': Encryptor.get_public_key_as_string(v['public_key']),
                    'symmetric_key': ''
                }

        with open(location + username + file_name + '.txt', 'wb') as f:
            f.write(json.dumps(res).encode())

    @classmethod
    def deserialize(cls, username, location: str = 'data/', file_name: str = '_contacts_to_keys'):
        try:
            with open(location + username + file_name + '.txt', 'rb') as f:
                file_content = f.read()
                if file_content != b'':
                    res = json.loads(file_content)
                    for k, v in res.items():
                        cls.get_instance().contacts_to_keys[k] = {
                            'public_key': Encryptor.load_public_key_from_string(v['public_key']),
                            'symmetric_key': v['symmetric_key']
                        }
        except FileNotFoundError:
            print('No such file')


    @classmethod
    def add_contact_public_key(cls, username: str, public_key):
        if isinstance(public_key, str):
            public_key = Encryptor.load_public_key_from_string(public_key)
        cls.get_instance().contacts_to_keys[username] = {
            'public_key':  public_key,
            'symmetric_key': cls.get_instance().contacts_to_keys[username]['symmetric_key']
        }

    @classmethod
    def get_contact_public_key(cls, username: str):
        return ContactsToKeys.get_instance().contacts_to_keys[username]['public_key']

    @classmethod
    def add_contact_symmetric_key(cls, username: str, symmetric_key):
        if isinstance(symmetric_key, bytes):
            symmetric_key = symmetric_key.decode()
        cls.get_instance().contacts_to_keys[username] = {
            'public_key': cls.get_instance().contacts_to_keys[username]['public_key'],
            'symmetric_key':  symmetric_key
        }

    @classmethod
    def get_contact_symmetric_key(cls, username: str):
        return ContactsToKeys.get_instance().contacts_to_keys[username]['symmetric_key']

    @classmethod
    def delete_all_records(cls):
        cls.get_instance().contacts_to_keys = {}


# singleton
class Contacts:
    class __Contacts:
        def __init__(self, contacts: List[Contact] = None, ):
            if contacts is None:
                self.contacts = []
            else:
                self.contacts = contacts

        def __repr__(self):
            return json.dumps(self, default=lambda o: o.__dict__, indent=3)

    _instance: __Contacts = None

    def __init__(self, contacts: List[Contact] = None):
        Contacts._instance = Contacts.__Contacts(contacts)

    @classmethod
    def from_json(cls, arg):
        return Contacts(contacts=list(map(Contact.from_json, arg["contacts"])))

    @classmethod
    def serialize(cls, username, location: str = 'data/', file_name: str = '_contacts'):
        with open(location + username + file_name + '.txt', 'w') as f:
            f.write(str(cls.get_instance()))
        ContactsToKeys.serialize(username)

    @classmethod
    def deserialize(cls, username, location: str = 'data/', file_name: str = '_contacts'):
        try:
            with open(location + username + file_name + '.txt', 'r') as f:
                file_content = f.read()
                if file_content != '':
                    Contacts.from_json(json.loads(file_content))
            ContactsToKeys.deserialize(username)
        except FileNotFoundError:
            cls._instance = cls.__Contacts()
        finally:
            print(Contacts.get_instance())
            print(ContactsToKeys.get_instance())

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
            if not cls.contact_exists(contact.username):
                cls.get_instance().contacts.append(contact)
        else:
            raise TypeError

    @classmethod
    def contact_exists(cls, username):
        return any(contact.username == username for contact in cls.get_instance().contacts)


    @classmethod
    def delete_all_contacts(cls):
        cls.get_instance().contacts = []
