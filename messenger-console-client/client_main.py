import json

from encryptor import Enscryptor
from app_client import Client
import user

request_sender = 'gleb'


def main():
    #send_msgs()
    client = Client()
    content = {'username': 'gleb', 'password': 'website', 'public_key': 'pkey', 'email': 'example@g.com'}
    client.run(action='register', request_content=content, request_sender=request_sender)


def send_msgs():
    inpt = ''
    #enscr = Enscryptor()
    pub_key, pr_key = Enscryptor.generate_keys()
    while inpt != 'q':
        inpt = input('Input message: ')
        msg = user.UserMessage(sender='gleb', recipient='ivan', content=inpt)
        client = Client()
        msg = Enscryptor.simple_encrypt_message(json.dumps(msg.as_dict()))
        client.run(action='message', request_content=msg.as_dict(), request_sender=request_sender)

        client = Client()
        client.run(action='getnewmsgs', request_sender=request_sender)

if __name__ == "__main__":
    main()