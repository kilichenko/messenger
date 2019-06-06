from user import User, Users
from user_message import UserMessage
import json


class Request:
    # expects content is username
    def _search(self):
        if self.content in Users.get_users():
            self.response['key'] = Users.get_public_key(self.content)

    # expects content is dict {content: str, sender: str, recipient: str}
    def _message(self):
        message = UserMessage.parse_from_dict(self.content)
        message_recipient = Users.get_user(message.recipient)
        message_recipient.add_undelivered_message(message)
        message_recipient.add_msg_to_dialog(message.sender, message)

    # expects content is dict {message_array: [{content: str, sender: str, recipient: str}]}
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

    # expects content is dict {username: str, password: str, public_key: str, email: str}
    def _register(self):
        username = self.content['username']
        password = self.content['password']
        public_key = self.content['public_key']
        email = self.content['email']
        if username in Users.get_users():
            self.status = Request.status_codes['LOGIN_NOT_AVAILABLE']
            return ''

        usr = User(username=username, password=password, public_key=public_key, email=email)
        Users.add_user(usr)

    def _connect(self, request_sender):
        pass

    def get_status_code(self) -> int:
        return self.status

    status_codes = {'OK': 0, 'ERR': 1, 'LOGIN_NON_AVAILABLE': 2, 'INVALID_ACTION': 3}

    def __init__(self, sender: str, action: str, content: dict):
        self.sender: str = sender
        self.action: str = action
        self.content: dict = content
        self.status: int = Request.status_codes.get('OK')
        self.response = {}
        self.valid_actions = {'search': self._search,
                              'message': self._message,
                              'save': self._save,
                              'getnewmsgs': self._getnewmsgs,
                              'getallmsgs': self._getallmsgs,
                              'register': self._register,
                              'connect': self._connect}

    def process_request(self) -> str:
        if self.action not in self.valid_actions:
            self.status = Request.status_codes['INVALID_ACTION']
            return ''

        self.valid_actions[self.action]()
        return json.dumps(self.response)
