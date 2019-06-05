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
        response = ''
        if self.action == 'message':
            pass
        elif self.action == 'getallmsgs':
            pass
        elif self.action == 'getnewmsgs':
            content = json.loads(self.content)
            if content['content']:
                self.client.run(action='save', content=self.content, sender='gleb')
                for msg in content['content']:
                    response += msg.get('sender') + ': ' + msg.get('content') + '\n'

        return response
