import socketserver as ss
from web_socket_util import get_local_ip, TCPDatagramHandler
from display_util import print_notification


if __name__ == "__main__":
    host, _ = get_local_ip()
    with ss.TCPServer((host, 0), TCPDatagramHandler) as server:
        port = server.socket.getsockname()[1]
        print_notification("Beginning server on port {}".format(port))
        server.serve_forever()
