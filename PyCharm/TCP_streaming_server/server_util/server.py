import socketserver
import time
from multiprocessing import Queue

from video_util.data import VideoStream
from .datapacket_util import VideoInitDatagram, VideoStreamDatagram


class VideoStreamingServer(socketserver.TCPServer):
    def __init__(self, device_identifier: str, cam_q: Queue, stream_type: VideoStream, **kwargs):
        super().__init__(RequestHandlerClass=VideoStreamingHandler, **kwargs)
        self.stream_type = stream_type
        self.dev = device_identifier
        self.cam_q = cam_q
        self.fps = 0

        print('Starting server {} @ {} on port {}'.format(device_identifier,
                                                          self.socket.getsockname()[0], self.socket.getsockname()[1]))


class VideoStreamingHandler(socketserver.StreamRequestHandler):
    """Request Handler for handling video streaming"""

    def __init__(self, request, client_address, server):
        self.wbufsize = 3072000
        super().__init__(request, client_address, server)

    def handle(self):

        print("Client connected")

        # region Sets up the video streams

        depth_stream_info = VideoInitDatagram(self.server.dev, [self.server.stream_type])

        self.wfile.write((depth_stream_info.to_json() + '~~~\n').encode('utf-8'))

        # endregion

        datagram = None
        j = ""
        first = True

        while True:
            start = time.time()
            try:
                data = self.server.cam_q.get()
                if first:
                    first = False
                    datagram = VideoStreamDatagram(self.server.dev, self.server.stream_type.name, data,
                                                   self.server.stream_type.dtype)
                else:
                    datagram.frame = data

                j = datagram.to_json()
                self.wfile.write((j + '~~~\n').encode('utf-8'))
            except Exception as e:
                print(e)
                break

            self.server.fps = 1 / (time.time() - start)
