import json
import request
import client_session
# from client_session import ClientSession
from contact import ContactsToKeys, Contacts, Contact
from encryptor import Encryptor
from user_message import UserMessage


class ResponseHandler:
    valid_actions = ('search', 'message', 'getnewmsgs', 'getallmsgs', 'register',
                     'connect', 'authenticate', 'log_out', 'block')
    status_codes = {'OK': 0, 'ERR': 1, 'LOGIN_NOT_AVAILABLE': 2, 'INVALID_ACTION': 3, 'WRONG_PASSWORD': 4,
                    'USER_DO_NOT_EXIST': 5, 'AUTHENTICATION_REQUIRED': 6, 'CONNECT_ALREADY_PENDING': 7}

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
        elif self.response_status == 7:
            print('CONNECT_ALREADY_PENDING')
            return ''

        if self.action not in ['authenticate', 'register']:
            key = client_session.ClientSession.get_server_symmetric_key()
            self.content = Encryptor.symmetrical_decrypt(key=key, message=self.content)
            self.content = json.loads(self.content)

        print(self.action, ' response content: ', type(self.content), self.content)

        result = ''
        if self.action == 'message':
            pass
        elif self.action == 'authenticate':
            client_session.ClientSession.set_server_symmetric_key(self.content['key'])
        elif self.action == 'search':

            ContactsToKeys.add_contact_public_key(username=self.content['username'],
                                                  public_key=self.content['key'])
        # expects {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getallmsgs':
            pass
        # expects {response_content: {message_array: [{content: str, sender: str, recipient: str}]}}
        elif self.action == 'getnewmsgs':
            accept_contact = True

            # content = json.loads(self.content)
            for msg in self.content['message_array']:
                sender = msg['sender']
                recipient = msg['recipient']
                content = msg['content']

                # new message from a contact
                if Contacts.contact_exists(sender) and Contacts.get_contact(sender).is_connected():
                    Contacts.get_contact(sender).add_message(UserMessage(sender=sender,
                                                                         recipient=recipient, content=content))
                    print(msg)
                # response to a connect request
                elif Contacts.contact_exists(sender) and not Contacts.get_contact(sender).is_connected():
                    sender = Contacts.get_contact(sender)
                    sender.is_connected()
                    private_key = client_session.ClientSession.get_client_private_key()
                    decrypted_key = Encryptor.asymmetric_decrypt_message(key=private_key, message=content['key'])
                    ContactsToKeys.add_contact_symmetric_key(symmetric_key=decrypted_key,
                                                             username=sender.get_username())
                    ContactsToKeys.add_contact_public_key(public_key=content['public_key'],
                                                          username=sender.get_username())
                # accepting incoming connect request
                elif accept_contact:
                    Contacts.add_contact(Contact(sender, connected=True))
                    sender = Contacts.get_contact(sender)
                    private_key = client_session.ClientSession.get_client_private_key()
                    content = json.loads(content)
                    decrypted_key = Encryptor.asymmetric_decrypt_message(key=private_key, message=content['key'])
                    ContactsToKeys.add_contact_symmetric_key(symmetric_key=decrypted_key,
                                                             username=sender.get_username())
                    ContactsToKeys.add_contact_public_key(public_key=content['public_key'],
                                                          username=sender.get_username())
                    content = {}
                    content['key'] = ContactsToKeys.get_contact_symmetric_key(sender.get_username())
                    content['pubic_key'] = Encryptor.\
                        get_public_key_as_string(client_session.ClientSession.get_client_public_key())
                    content = json.dumps(content)

                    req = request.Request(action='connect',
                                          request_content=UserMessage(recipient=sender, sender=recipient,
                                                                      content=content).as_dict(),
                                          request_sender=sender)
                    req.send_request()
                # rejecting incoming connect request
                else:
                    req = request.Request(action='block',
                                          request_content={'username': sender},
                                          request_sender=sender)
                    req.send_request()

        elif self.action == 'register':
            pass
        elif self.action == 'delete_account':
            Contacts.delete_all_contacts()
            ContactsToKeys.delete_all_records()

        return result
