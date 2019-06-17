import base64
import json

import client_session
from client_session import ClientSession
from contact import Contacts, Contact, ContactsToKeys
from encryptor import Encryptor
from request import Request
from user_message import UserMessage


def register(username, password, email):
    public_key, private_key = Encryptor.generate_keys()
    Encryptor.save_private_key(private_key=private_key, file_name=username + '_private_key')
    Encryptor.save_public_key(public_key=public_key, file_name=username + '_public_key')
    content = {'username': username, 'password': password,
               'public_key': Encryptor.get_public_key_as_string(public_key), 'email': email}
    request = Request(action='register', request_content=content, request_sender=request_sender)
    request.send_request()


def send_msgs():
    inpt = ''
    server_pub_key = Encryptor.load_public_key()

    while inpt != 'q':
        inpt = input('Input message: ')
        request = Request(action='message', request_content={}, request_sender=request_sender)
        request.send_request()

        request = Request(action='getnewmsgs', request_sender=request_sender)
        request.send_request()


def send_message(content, sender, recipient):
    request = Request(action='message',
                      request_content=UserMessage(request_sender, recipient, content).as_dict(),
                      request_sender=sender)
    request.send_request()


def connect_to_recipient(recipient: str, sender: str):
    key = Encryptor.generate_symmetric_key()
    encrypted_key = Encryptor.asymmetric_encrypt_message(key=ContactsToKeys.get_contact_public_key(recipient),
                                                         message=key)
    Contacts.add_contact(Contact(recipient))
    content = {}
    content['key'] = encrypted_key
    content['public_key'] = Encryptor. \
        get_public_key_as_string(client_session.ClientSession.get_client_public_key())
    request = Request(action='connect',
                      request_content=UserMessage(request_sender, recipient, json.dumps(content)).as_dict(),
                      request_sender=sender)
    request.send_request()


def search(username, sender):
    request = Request(action='search',
                      request_content={'username': username},
                      request_sender=sender)
    request.send_request()


def recieve_msgs(sender):
    request = Request(action='getnewmsgs',
                      request_content={},
                      request_sender=sender)
    request.send_request()


def delete_account():
    request = Request(action='delete_account',
                      request_content={'username': ClientSession.get_instance().username,
                                       'password': ClientSession.get_instance().password},
                      request_sender=ClientSession.get_instance().username)
    request.send_request()


request_sender = 'ivan'


def main():
    #register(request_sender, request_sender, 'ggteeg@gmail.com')

    ClientSession(request_sender, request_sender)
    Contacts.deserialize(request_sender)
    ClientSession.establish_session()

    #search('ivan', request_sender)
    #connect_to_recipient('ivan', request_sender)
    recieve_msgs(request_sender)
    Contacts.serialize(request_sender)


if __name__ == "__main__":
    main()
