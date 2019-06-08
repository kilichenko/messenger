import socket
import ssl
import selectors
import traceback
import request_sender
from typing import Dict


class Request:
    def __init__(self, action, request_sender, host='192.168.1.40', port=65000, request_content=None):
        self.sel = selectors.DefaultSelector()
        self.host, self.port = host, port
        self.action = action
        self.request_sender = request_sender
        self.request_content = request_content

    def send_request(self):
        self._start_connection()

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

    def _create_request(self) -> Dict:
        if self.action in ('search', 'message', 'save', 'getnewmsgs', 'getallmsgs', 'register'):
            return {'type': "text/json", 'encoding': "utf-8",
                    'request_body': {'action': self.action, 'request_content': self.request_content,
                                     'request_sender': self.request_sender}}
        else:
            return {'type': "binary/custom-client-binary-type", 'encoding': "binary",
                    'request_body': bytes(self.action + self.request_content, encoding="utf-8")}

    def _start_connection(self):
        addr = (self.host, self.port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = request_sender.RequestSender(self.sel, sock, addr, self._create_request())
        self.sel.register(sock, events, data=message)


