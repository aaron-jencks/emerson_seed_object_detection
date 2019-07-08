import socketserver


class VideoStreamingHandler(socketserver.StreamRequestHandler):
    """Request Handler for handling video streaming"""


class VideoStreamingServer(socketserver.TCPServer):
    pass
