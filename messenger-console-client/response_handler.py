import json
import request


class ResponseHandler:
    valid_actions = ('search', 'message', 'save', 'getnewmsgs', 'getallmsgs', 'register', 'connect')
    status_codes = {0: 'OK', 1: 'ERR', 2: 'LOGIN_NOT_AVAILABLE', 3: 'INVALID_ACTION'}

    def __init__(self, action: str, content: str, response_status: int):
        self.action: str = action
        self.content: str = content
        self.response_status: int = response_status
        #self.client: request.Request = request.Request()

    def process_response(self) -> str:
        result = ''
        if self.action == 'message':
            pass
        elif self.action == 'save':
            pass
        elif self.action == 'search':
            pass
        #expects {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getallmsgs':
            pass
        # expects {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getnewmsgs':
            content = json.loads(self.content)
            for msg in content['message_array']:
                result += msg.get('sender') + ': ' + msg.get('content') + '\n'
        elif self.action == 'register':
            if ResponseHandler.status_codes[self.response_status] == 'LOGIN_NOT_AVAILABLE':
                print('LOGIN_NOT_AVAILABLE')
        return result