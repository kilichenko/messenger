from server import Server
from user import Users


def main():
    Users.deserialize()
    server = Server('192.168.1.40', 65000)
    server.run()
    Users.serialize()


if __name__ == "__main__":
    main()
