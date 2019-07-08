import socketserver as ss
import socket
import json
import numpy as np

from display_util import print_error, print_info, print_notification, print_warning


def get_local_ip():
    """Finds the localhost ip address used for connecting to the LAN."""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print_info("You're computer's hostname is: {}".format(hostname))
    print_info("You're computer's local ip-address is: {}".format(ip))
    return hostname, ip


class TCPDatagramHandler(ss.StreamRequestHandler):
    """Used to process the requests made by clients"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_preparation_unit

    def handle(self):
        """Handles the requests made by the clients"""
        print_notification("Handling request from {}".format(self.client_address[0]))
        raw = self.rfile.readline()
        print_info("Raw data is: {}".format(raw))
        command = json.loads(raw)
        print_notification("Received packet containing {}".format(command))
        self.wfile.write(bytes(json.dumps({'message': 'Thank you',
                                           'frame': np.zeros(shape=(25, 40), dtype=int).tolist()}) + '\n',
                               'utf-8'))
