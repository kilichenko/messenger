import base64

from client_session import ClientSession
from contact import Contacts, Contact
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


def generate_new_keys():
    ivan_pub_key, ivan_pr_key = Encryptor.generate_keys()
    Encryptor.save_public_key(ivan_pub_key, file_name='ivan_public_key')
    Encryptor.save_private_key(ivan_pr_key, file_name='ivan_private_key')
    gleb_pub_key, gleb_pr_key = Encryptor.generate_keys()
    Encryptor.save_public_key(gleb_pub_key, file_name='gleb_public_key')
    Encryptor.save_private_key(gleb_pr_key, file_name='gleb_private_key')


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
    encrypted_key = Encryptor.asymmetric_encrypt_message(key=Contacts.get_public_key(recipient),
                                                         message=key)
    Contacts.add_pending_connect(Contact(recipient))
    request = Request(action='connect',
                      request_content=UserMessage(request_sender, recipient, encrypted_key).as_dict(),
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


request_sender = 'ivan'


def main():
    ClientSession(request_sender, request_sender)
    Contacts.deserialize(request_sender)
    ClientSession.establish_session()
    #search('ivan', 'gleb')
    #connect_to_recipient('ivan', 'gleb')
    recieve_msgs(request_sender)
    Contacts.serialize(request_sender)

    # register('gleb', 'gleb', 'mail.@gmail.com')
    # register('ivan', 'ivan', 'mail.@gmail.com')


if __name__ == "__main__":
    main()
