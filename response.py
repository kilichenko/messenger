import json
import app_client


class Response:
    #valid_actions = ('search', 'message', 'save', 'getnewmsgs', 'getallmsgs', 'register', 'connect')
    status_codes = {'OK': 0, 'ERR': 1}

    def __init__(self, action: str, content: str):
        self.action: str = action
        self.content: str = content
        self.client: app_client.Client = app_client.Client()

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
            if content['message_array']:
                #self.client.run(action='save', request_content=content['response_content']['message_array'], request_sender='gleb')
                self.client.run(action='save', request_content=self.content,
                                request_sender='gleb')
                for msg in content['message_array']:
                    result += msg.get('sender') + ': ' + msg.get('content') + '\n'
        elif self.action == 'register':
            pass
        elif self.action == 'register':
            pass
        return result
