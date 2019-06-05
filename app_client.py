import socket
import selectors
import traceback
import libclient


class Client:
    def __init__(self, host='192.168.1.40', port=65000):
        self.sel = selectors.DefaultSelector()
        self.host, self.port = host, port


    @staticmethod
    def create_request(action, sender, content, receiver):
        if action in ('search', 'message', 'save', 'getnewmsgs', 'getallmsgs', 'register'):
            return {'type': "text/json", 'encoding': "utf-8",
                    'content': {'action': action, 'content': content, 'sender': sender, 'receiver': receiver}}
        else:
            return {'type': "binary/custom-client-binary-type", 'encoding': "binary",
                    'content': bytes(action + content, encoding="utf-8")}

    def start_connection(self, host, port, request):
        addr = (host, port)
        #print("starting connection to", addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = libclient.Message(self.sel, sock, addr, request)
        self.sel.register(sock, events, data=message)

    def run(self, action, sender, content=None, receiver=None):
        request = self.create_request(action=action, content=content,
                                      sender=sender, receiver=receiver)
        self.start_connection(self.host, self.port, request)

        try:
            while True:
                events = self.sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                    except Exception:
                        print(
                            "main: error: exception for",
                            f"{message.addr}:\n{traceback.format_exc()}",
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
