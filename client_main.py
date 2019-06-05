from app_client import Client

sender, receiver = 'ivan', 'gleb'
content = ''
action = 'getnewmsgs'


def main():
    msg = ''
    while msg != 'q':
        msg = input('Input message: ')
        client = Client()
        client.run(action=action, content=msg, sender=sender, receiver=receiver)


def get_sender():
    return sender


if __name__ == "__main__":
    main()