import base64

from cryptography.hazmat.primitives import serialization

from encrytor import Encryptor
from server_session import ServerSession
from user import User, Users, UsersToPublicKeys
from user_message import UserMessage
from typing import Dict
import json


class ResponseCreator:
    # expects content is {username: str}
    def _search(self):
        if Users.user_exists(self.content['username']):
            self.response['key'] = Encryptor.get_public_key_as_string(Users.get_public_key(self.content['username']))
            self.response['username'] = self.content['username']
        else:
            self.status = ResponseCreator.status_codes['USER_DO_NOT_EXIST']

    # expects content is {content: str, sender: str, recipient: str}
    def _message(self):
        message = UserMessage(recipient=self.content['recipient'],
                              sender=self.content['sender'],
                              content=self.content['content'])
        message.set_timestamp()
        try:
            message_recipient = Users.get_user(message.recipient)
            message_recipient.add_undelivered_message(message)
        except KeyError:
            self.status = ResponseCreator.status_codes['USER_DO_NOT_EXIST']

    # expects content is {message_array: [{content: str, sender: str, recipient: str}]}
    def _save(self):
        request_content = json.loads(self.content)
        if request_content['response_content']['message_array']:
            for msg in request_content['response_content']['message_array']:
                msg = UserMessage.parse_from_dict(json.loads(self.content))
                message_sender = Users.get_user(msg.sender)
                message_sender.add_msg_to_dialog(msg.recipient, msg)

    # expects empty content
    # returns {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
    def _getnewmsgs(self):
        msg_list = []
        msgs = Users.get_user(self.sender).get_undelivered_messages()
        while len(msgs) != 0:
            msg = msgs.pop()
            msg_list.append(msg.as_dict())
        self.response['message_array'] = msg_list

    # expects empty content
    # returns {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
    def _getallmsgs(self):
        msg_list = []
        dialogs = Users.get_user(self.sender).get_all_dialogs()
        for k, v in dialogs.items():
            for msg in v.get_messages():
                msg_list.append(msg.as_dict())
        self.response['message_array'] = msg_list

    # expects content is {username: str, password: str, public_key: str, email: str}
    def _register(self):
        username = self.content['username']
        if Users.user_exists(username):
            self.status = ResponseCreator.status_codes['LOGIN_NOT_AVAILABLE']
            return
        password = self.content['password']
        public_key = self.content['public_key']
        email = self.content['email']
        usr = User(username=username,
                   password=Encryptor.hash_message(password.encode()).decode(), email=email)
        Users.add_user(usr)
        UsersToPublicKeys.add_user_public_key(username, public_key)

    # block a user
    # expects {username: str}
    def _block(self, request_sender):
        pass

    # expects content is {username: str, password: str}
    # returns {key: str}
    def _authenticate(self):
        username = self.content['username']
        if not Users.user_exists(username):
            self.status = ResponseCreator.status_codes['USER_DO_NOT_EXIST']
            return
        user = Users.get_user(username)
        password = Encryptor.asymmetric_decrypt_message(key=ServerSession.get_private_key(),
                                                        message=self.content['password'])
        if user.check_password(password):
            key = Encryptor.generate_symmetric_key()
            ServerSession.add_client_session_key(user.get_username(), key)
            pub_k = UsersToPublicKeys.get_public_key(username)
            encrypted_key = Encryptor.asymmetric_encrypt_message(key=pub_k, message=key)
            self.response = {'key': encrypted_key}
        else:
            self.status = ResponseCreator.status_codes['WRONG_PASSWORD']

    def _log_out(self):
        pass

    # used to get symmetrical key from recipient
    # expects content {key: str}
    def _connect(self):
        message = UserMessage(recipient=self.content['recipient'],
                              sender=self.content['sender'],
                              content=self.content['content'])
        message.set_timestamp()
        try:
            message_recipient = Users.get_user(message.recipient)
            message_recipient.add_undelivered_message(message)
        except KeyError:
            self.status = ResponseCreator.status_codes['USER_DO_NOT_EXIST']

    def get_status_code(self) -> int:
        return self.status

    status_codes = {'OK': 0, 'ERR': 1, 'LOGIN_NOT_AVAILABLE': 2, 'INVALID_ACTION': 3, 'WRONG_PASSWORD': 4,
                    'USER_DO_NOT_EXIST': 5, 'AUTHENTICATION_REQUIRED': 6}

    def __init__(self, sender: str, action: str, content):
        self.status: int = ResponseCreator.status_codes.get('OK')
        self.sender: str = sender
        self.action: str = action
        self.content: dict = content
        self.response = {}
        self.valid_actions = {'search': self._search,
                              'message': self._message,
                              'getnewmsgs': self._getnewmsgs,
                              'getallmsgs': self._getallmsgs,
                              'register': self._register,
                              'authenticate': self._authenticate,
                              'log_out': self._log_out,
                              'connect': self._connect,
                              'block': self._block}

    def _decrypt_from_client(self):
        if self.action not in ['authenticate', 'register']:
            key = ServerSession.get_client_session_key(self.sender)
            self.content = Encryptor.symmetrical_decrypt(key=key, message=self.content)
            self.content = json.loads(self.content)

    def _encrypt_for_client(self):
        if self.action not in ['authenticate', 'register']:
            key = ServerSession.get_client_session_key(self.sender)
            self.response = Encryptor.symmetrical_encrypt(key=key, message=json.dumps(self.response))
            self.response = self.response.decode()

    def process_request(self) -> Dict:
        request_is_valid = True

        if not ServerSession.session_established(self.sender) and self.action not in ['authenticate', 'register']:
            self.status: int = ResponseCreator.status_codes.get('AUTHENTICATION_REQUIRED')
            request_is_valid = False

        if self.action not in self.valid_actions:
            self.status = ResponseCreator.status_codes['INVALID_ACTION']
            request_is_valid = False

        if request_is_valid:
            self._decrypt_from_client()
            print('decoded request: ', self.content)
            self.valid_actions[self.action]()
            self._encrypt_for_client()

        return self.response
