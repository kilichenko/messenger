from app_client import Client
import user

request_sender = 'gleb'


def main():
    inpt = ''
    while inpt != 'q':
        inpt = input('Input message: ')
        msg = user.UserMessage(sender='gleb', recipient='ivan', content=inpt)
        client = Client()
        client.run(action='message', request_content=msg.asdict(), request_sender=request_sender)

        client = Client()
        client.run(action='getnewmsgs', request_sender=request_sender)


if __name__ == "__main__":
    main()