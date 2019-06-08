import json

from encryptor import Encryptor
from app_client import Request
import user

request_sender = 'gleb'


def main():
    server_pub_key = Encryptor.load_public_key('public_key.pem')

    #ivan_pub_key, ivan_pr_key = Encryptor.generate_keys()
    #Encryptor.save_private_key(ivan_pr_key, 'ivan_private_key.pem')
    #Encryptor.save_public_key(ivan_pr_key, 'ivan_public_key.pem')

    #send_msgs()
    #content = {'username': 'gleb', 'password': 'website', 'public_key': 'pkey', 'email': 'example@g.com'}
    #request = Request(action='register', request_content=content, request_sender=request_sender)
    #request.send_request()



def send_msgs():
    inpt = ''
    server_pub_key = Encryptor.load_public_key('public_key.pem')

    while inpt != 'q':
        inpt = input('Input message: ')
        request = Request(action='message', request_content={}, request_sender=request_sender)
        request.send_request()

        request = Request(action='getnewmsgs', request_sender=request_sender)
        request.send_request()

if __name__ == "__main__":
    main()