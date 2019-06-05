from app_client import Client
import time
import threading

sender, receiver = 'gleb', 'ivan'
content = ''
action = 'message'


def main():
    getter = threading.Thread(target=getter_thread)
    getter.run()
    msg = ''
    while msg != 'q':
        msg = input('Input message: ')
        client = Client()
        client.run(action=action, content=msg, sender=sender, receiver=receiver)


def getter_thread():
    while True:
        time.sleep(2)
        client = Client()
        client.run(action='getnewmsgs', sender=sender)



def get_sender():
    return sender


if __name__ == "__main__":
    main()