import base64

from cryptography.hazmat.primitives import serialization

from encrytor import Encryptor
from server_session import ServerSession
from user import User, Users, UsersToPublicKeys
from user_message import UserMessage
import json


class ResponseCreator:
    # expects content is {username: str}
    def _search(self):
        if self.content['username'] in Users.get_users():
            self.response['key'] = Users.get_public_key(self.content['username'])
        else:
            self.status = ResponseCreator.status_codes['USER_DO_NOT_EXIST']

    # expects content is {content: str, sender: str, recipient: str}
    def _message(self):
        key = ServerSession.get_client_session_key(username=self.content['sender'])
        decrypted = Encryptor.symmetrical_decrypt(
            key=key,
            message=self.content['content']
        )
        print(decrypted)
        message = UserMessage.parse_from_dict(self.content)
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

    def get_status_code(self) -> int:
        return self.status

    status_codes = {'OK': 0, 'ERR': 1, 'LOGIN_NOT_AVAILABLE': 2, 'INVALID_ACTION': 3, 'WRONG_PASSWORD': 4,
                    'USER_DO_NOT_EXIST': 5}

    def __init__(self, sender: str, action: str, content: dict):
        self.sender: str = sender
        self.action: str = action
        self.content: dict = content
        self.status: int = ResponseCreator.status_codes.get('OK')
        self.response = {}
        self.valid_actions = {'search': self._search,
                              'message': self._message,
                              'getnewmsgs': self._getnewmsgs,
                              'getallmsgs': self._getallmsgs,
                              'register': self._register,
                              'authenticate': self._authenticate,
                              'block': self._block}

    def process_request(self) -> str:
        if self.action not in self.valid_actions:
            self.status = ResponseCreator.status_codes['INVALID_ACTION']
            return ''

        self.valid_actions[self.action]()
        return json.dumps(self.response)
