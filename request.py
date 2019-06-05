import u2kht
from user import User, Users
from user_message import UserMessage
import json


class Request:
    #valid_actions = ('search', 'message', 'save', 'getnewmsgs', 'getallmsgs', 'register', 'connect')
    status_codes = {'OK': 0, 'ERR': 1}

    def __init__(self, sender: str,  action: str, content: str):
        self.sender: str = sender
        self.action: str = action
        self.content: str = content
        self.status: int = Request.status_codes.get('OK')

    def get_status_code(self) -> int:
        return self.status

    def process_request(self) -> str:
        response = {}

        request_sender = Users.get_user(self.sender)

        #expects content is username
        if self.action == "search":
            if self.content in u2kht.u2k:
                response['key'] = u2kht.u2k[self.content]
        #expects content is dict {content: str, sender: str, recipient: str}
        elif self.action == 'message':
            #Why self.content is dict?!
            message = UserMessage.parse_from_dict(self.content)
            message_recipient = Users.get_user(message.recipient)
            message_recipient.add_undelivered_message(message)
            message_recipient.add_msg_to_dialog(message.sender, message)
        #expects content is dict {message_array: [{content: str, sender: str, recipient: str}]}
        elif self.action == 'save':
            request_content = json.loads(self.content)
            if request_content['response_content']['message_array']:
                for msg in request_content['response_content']['message_array']:
                    msg = UserMessage.parse_from_dict(json.loads(self.content))
                    message_sender = Users.get_user(msg.sender)
                    message_sender.add_msg_to_dialog(msg.recipient, msg)
        #expects empty content
        #returns {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getallmsgs':
            msg_list = []
            dialogs = request_sender.get_all_dialogs()
            for k, v in dialogs.items():
                for msg in v.get_messages():
                    msg_list.append(msg.asdict())
            response = {'message_array': msg_list}
        #expects empty content
        #returns {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getnewmsgs':
            msg_list = []
            msgs = request_sender.get_undelivered_messages()
            while len(msgs) != 0:
                msg = msgs.pop()
                msg_list.append(msg.asdict())
            response = {'message_array': msg_list}
        #expects content is dict {login: str, password: str, public_key: str}
        elif self.action == 'register':
            pass
        elif self.action == 'connect':
            pass

        return json.dumps(response)
