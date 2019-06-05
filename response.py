import json
import app_client


class Response:
    #valid_actions = ('search', 'message', 'save', 'getnewmsgs', 'getallmsgs', 'register')
    status_codes = {'OK': 0, 'ERR': 1}

    def __init__(self, action: str, content: str):
        self.action: str = action
        self.content: str = content
        self.client: app_client.Client = app_client.Client()

    def process_response(self) -> str:
        if self.action == 'message':
            pass
        elif self.action == 'getallmsgs':
            self.client.run(action='save', content=self.content, sender='gleb')
        elif self.action == 'getnewmsgs':
            self.client.run(action='save', content=self.content, sender='gleb')
        return self.content
