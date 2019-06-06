import sys
import socket
import selectors
import traceback
import ssl

from message import Message

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sel = selectors.DefaultSelector()

    def run(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind((self.host, self.port))
        lsock.listen()
        print("listening on", (self.host, self.port))
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            print(
                                "main: error: exception for",
                                f"{message.addr}:\n{traceback.format_exc()}",
                            )
                            message.close()
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()


    def accept_wrapper(self, sock):
        #context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        #context.load_cert_chain(certfile="cert.pem")
        #context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        #context.load_cert_chain('cert.pem')
        #context.check_hostname = False
        #ssock = context.wrap_socket(sock, server_side=True)
        conn, addr = sock.accept()
        print("accepted connection from", addr)
        conn.setblocking(False)
        message = Message(self.sel, conn, addr)
        self.sel.register(conn, selectors.EVENT_READ, data=message)