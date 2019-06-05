from app_client import Client
import time

sender, receiver = 'ivan', 'gleb'
content = ''
action = 'message'


def main():
    msg = ''
    while msg != 'q':
        msg = input('Input message: ')
        client = Client()
        client.run(action=action, content=msg, sender=sender, receiver=receiver)
        client = Client()
        client.run(action='getnewmsgs', sender=sender)

def get_sender():
    return sender


if __name__ == "__main__":
    main()