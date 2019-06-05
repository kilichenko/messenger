"""Main module
"""

from user import User, Users
from server import Server
from user_message import UserMessage

def add_dull_data():
    gleb = User('gleb', '1111', 'gefgerger')
    ivan = User('ivan', '2222', 'bggfdfgf')
    vova = User('vova', '3333', 'dfgfdgfsg')
    ivan.add_undelivered_message(UserMessage('gleb', 'ivan', 'test message1'))
    ivan.add_undelivered_message(UserMessage('gleb', 'ivan', 'test message2'))

def main():
    add_dull_data()
    server = Server('192.168.1.40', 65000)
    server.run()


if __name__ == "__main__":
    main()
