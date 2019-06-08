import base64

from idna import unicode

from encryptor import Encryptor
from request import Request
from user_message import UserMessage


def load_keys():
    server_pub_key = Encryptor.load_public_key()
    gleb_pub_key = Encryptor.load_public_key_as_bytes(file_name='gleb_public_key')
    gleb_pr_key = Encryptor.load_private_key(file_name='gleb_public_key')


def register(username, password, public_key, email):
    content = {'username': username, 'password': password, 'public_key': public_key.decode(), 'email': email}
    request = Request(action='register', request_content=content, request_sender=request_sender)
    request.send_request()


def generate_new_keys():
    ivan_pub_key, ivan_pr_key = Encryptor.generate_keys()
    Encryptor.save_public_key(ivan_pub_key, file_name='ivan_public_key')
    Encryptor.save_private_key(ivan_pr_key, file_name='ivan_private_key')
    gleb_pub_key, gleb_pr_key = Encryptor.generate_keys()
    Encryptor.save_public_key(gleb_pub_key, file_name='gleb_public_key')
    Encryptor.save_private_key(gleb_pr_key, file_name='gleb_private_key')


request_sender = 'gleb'


def send_msgs():
    inpt = ''
    server_pub_key = Encryptor.load_public_key()

    while inpt != 'q':
        inpt = input('Input message: ')
        request = Request(action='message', request_content={}, request_sender=request_sender)
        request.send_request()

        request = Request(action='getnewmsgs', request_sender=request_sender)
        request.send_request()


def send_message(content, sender):
    request = Request(action='message', request_content=content, request_sender=sender)
    request.send_request()


def main():
    pub_k = Encryptor.load_public_key()
    gleb_pub_key = Encryptor.load_public_key(file_name='gleb_public_key')
    gleb_pr_key = Encryptor.load_private_key(file_name='gleb_private_key')

    message = b'fuck it'
    encrypted = Encryptor.asymmetric_encrypt_message(key=pub_k, message=message)
    print(type(encrypted), encrypted)
    coded = base64.b64encode(encrypted).decode('utf-8')
    print(coded)
    send_message(UserMessage(request_sender, 'ivan', coded).as_dict(), request_sender)



if __name__ == "__main__":
    main()
