import socketserver
import time
import numpy as np
from multiprocessing import Queue

from video_util.data import VideoStreamType, VideoStream
from .datapacket_util import VideoInitDatagram, VideoStreamDatagram


class VideoStreamingServer(socketserver.TCPServer):
    def __init__(self, device_identifier: str, cam_q: Queue, stream_type: VideoStream, **kwargs):
        super().__init__(RequestHandlerClass=VideoStreamingHandler, **kwargs)
        self.stream_type = stream_type
        self.dev = device_identifier
        self.cam_q = cam_q

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
                    datagram = VideoStreamDatagram(self.server.dev, self.server.stream_type.name, data)
                else:
                    datagram.frame = data

                # print('\rRunning at {} fps'.format(1 / (time.time() - start)), end='')
                # self.wfile.write((VideoStreamDatagram(self.server.dev, 'rgb', rgb).to_json() + '\n').encode('utf-8'))

                j = datagram.to_json()
                print('\rRunning at {} fps'.format(1 / (time.time() - start)), end='')
                self.wfile.write((j + '~~~\n').encode('utf-8'))
            except Exception as e:
                print(e)
                break

            print('\rRunning at {} fps'.format(1 / (time.time() - start)), end='')
        print('')
