import socket
import json
from display_util import print_notification, print_error, print_warning, print_info, get_input
from web_socket_util import get_local_ip

intermediary_data = ''.encode('utf-8')


def recv_packet(soc: socket.socket) -> bytes:
    global intermediary_data

    if len(intermediary_data.splitlines()) > 1:
        grams = intermediary_data.splitlines()
        intermediary_data = grams[1:]
        return grams[0]
    else:
        result = intermediary_data

        grams = soc.recv(1024)
        while '\n'.encode('utf-8') not in grams:
            result += grams
            grams = soc.recv(1024)

        loc = grams.find('\n'.encode('utf-8'))
        if loc >= 0:
            result += grams[:loc]
            if loc < len(grams) - 1:
                intermediary_data = grams[loc + 1:]
            else:
                intermediary_data = ''.encode('utf-8')

        print_notification('Received {} bytes'.format(len(result)))
        return result


if __name__ == "__main__":
    print_notification("Starting depth camera server client")
    hostname, _ = get_local_ip()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((hostname, int(get_input('Port Number? '))))
        while True:
            sock.send(bytes(json.dumps({'message':
                                        get_input('What would you like to say? ')}),
                            'utf-8') + bytes('\n', 'utf-8'))
            received = str(recv_packet(sock))
            print_info("Received data: {}".format(received))
