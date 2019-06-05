import u2kht
from user import User, Users
from user_message import UserMessage
import json


class Request:
    #valid_actions = ('search', 'message', 'save', 'getnewmsgs', 'getallmsgs', 'register')
    status_codes = {'OK': 0, 'ERR': 1}

    def __init__(self, sender: str, recipient: str, action: str, content: str):
        self.sender: str = sender
        self.recipient: str = recipient
        self.action: str = action
        self.content: str = content
        self.status: int = Request.status_codes.get('OK')

    def get_status_code(self) -> int:
        return self.status

    def process_request(self) -> str:
        response = {}

        request_sender = Users.get_user(self.sender)

        if self.action == "search":
            if self.content in u2kht.u2k:
                response['content'] = u2kht.u2k[self.content]
        elif self.action == 'message':
            request_recipient = Users.get_user(self.recipient)
            request_recipient.add_undelivered_message(UserMessage(self.sender, self.recipient, self.content))
            request_recipient.add_msg_to_dialog(self.recipient, UserMessage(self.sender, self.recipient, self.content))
            response = {'content': self.content, 'recipient': self.recipient}
        elif self.action == 'save':
            content = json.loads(self.content)
            if content['content']:
                for msg in content['content']:
                    msg = UserMessage(msg.get('sender'), msg.get('recipient'), msg.get('content'))
                    message_sender = Users.get_user(msg.sender)
                    message_sender.add_msg_to_dialog(msg.recipient, msg)
                response['content'] = self.content
        elif self.action == 'getallmsgs':
            msg_list = []
            dialogs = request_sender.get_all_dialogs()
            for k, v in dialogs.items():
                for msg in v.get_messages():
                    msg_list.append(msg.asdict())
            response['content'] = msg_list
        elif self.action == 'getnewmsgs':
            msg_list = []
            msgs = request_sender.get_undelivered_messages()
            while len(msgs) != 0:
                msg = msgs.pop()
                msg_list.append(msg.asdict())
            response['content'] = msg_list
        elif self.action == 'register':
            pass

        return json.dumps(response)
