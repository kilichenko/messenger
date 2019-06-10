import json
import request
import client_session
# from client_session import ClientSession
from contact import ContactsToPublicKeys, Contacts, Contact
from encryptor import Encryptor
from user_message import UserMessage


class ResponseHandler:
    valid_actions = ('search', 'message', 'getnewmsgs', 'getallmsgs', 'register',
                     'connect', 'authenticate', 'log_out', 'block')
    status_codes = {'OK': 0, 'ERR': 1, 'LOGIN_NOT_AVAILABLE': 2, 'INVALID_ACTION': 3, 'WRONG_PASSWORD': 4,
                    'USER_DO_NOT_EXIST': 5, 'AUTHENTICATION_REQUIRED': 6}

    def __init__(self, action: str, content: dict, response_status: int):
        self.action: str = action
        self.content: dict = content
        self.response_status: int = response_status

    def process_response(self) -> str:
        if self.response_status == 1:
            print('ERR')
            return ''
        elif self.response_status == 2:
            print('LOGIN_NOT_AVAILABLE')
            return ''
        elif self.response_status == 3:
            print('INVALID_ACTION')
            return ''
        elif self.response_status == 4:
            print('WRONG_PASSWORD')
            return ''
        elif self.response_status == 5:
            print('USER_DO_NOT_EXIST')
            return ''
        elif self.response_status == 6:
            print('AUTHENTICATION_REQUIRED')
            return ''

        if self.action not in ['authenticate', 'register']:
            key = client_session.ClientSession.get_server_symmetric_key()
            self.content = Encryptor.symmetrical_decrypt(key=key, message=self.content)
            self.content = json.loads(self.content)

        print(self.content)

        result = ''
        if self.action == 'message':
            pass
        elif self.action == 'authenticate':
            client_session.ClientSession.set_server_symmetric_key(self.content['key'])
        elif self.action == 'search':
            ContactsToPublicKeys.add_contact_public_key(username=self.content['username'],
                                                        public_key=self.content['key'])
        # expects {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getallmsgs':
            pass
        # expects {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getnewmsgs':
            acccept_contact = True

            #content = json.loads(self.content)
            for msg in self.content['message_array']:
                sender = msg['sender']
                recipient = msg['sender']
                content = msg['content']
                new_connections = []
                if Contacts.contact_exists(sender):
                    Contacts.get_contact(sender).add_message(UserMessage(sender=sender,
                                                                         recipient=recipient, content=content))
                    print(msg)
                elif Contacts.pending_connect_exists(sender):
                    Contacts.add_contact(Contact(sender))
                    Contacts.remove_pending_connect(sender)
                    client_session.ClientSession.add_recipient_symmetric_key(content)
                elif acccept_contact and sender not in new_connections:
                    new_connections.append(sender)
                    Contacts.add_contact(Contact(sender))
                    req = request.Request(action='connect',
                                          request_content=UserMessage(recipient=sender, sender=recipient,
                                                                      content=content).as_dict(),
                                          request_sender=sender)
                    req.send_request()
                else:
                    req = request.Request(action='block',
                                          request_content={},
                                          request_sender=sender)
                    req.send_request()

        elif self.action == 'register':
            pass

        return result
