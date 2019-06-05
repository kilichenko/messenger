from app_client import Client
import time
import threading

sender, receiver = 'ivan', 'gleb'
content = ''
action = 'message'


def main():
    getter = threading.Thread(target=getter_thread)
    #getter.run()
    msg = ''
    while msg != 'q':
        msg = input('Input message: ')
        client = Client()
        client.run(action=action, content=msg, sender=sender, receiver=receiver)


def getter_thread():
    while True:
        time.sleep(5)
        print('5 sec elapsed')


def get_sender():
    return sender


if __name__ == "__main__":
    main()