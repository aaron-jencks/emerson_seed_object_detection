import socketserver
import time
import numpy as np
from multiprocessing import Queue
from netifaces import interfaces, ifaddresses

from video_util.data import VideoStream, VideoStreamType
from .datapacket_util import VideoInitDatagram, VideoStreamDatagram


def find_ip():
    ints = interfaces()
    if 'wlp1s0' in ints:
        addr = ifaddresses('wlp1s0')
        print('Your ip is {}'.format(addr['addr']))
        return addr['addr']
    else:
        print('Your ip is localhost')
        return 'localhost'


class VideoStreamingServer(socketserver.TCPServer):
    def __init__(self, device_identifier: str, cam_q: Queue, stream_type: VideoStream, tx_q: Queue = None, **kwargs):
        super().__init__(RequestHandlerClass=VideoStreamingHandler, **kwargs)
        self.stream_type = stream_type
        self.dev = device_identifier
        self.cam_q = cam_q
        self.tx_q = tx_q
        self.fps = 0
        self.first = {}

        print('Starting server {} @ {} on port {}'.format(device_identifier,
                                                          self.socket.getsockname()[0], self.socket.getsockname()[1]))

        if tx_q is not None:
            self.tx_q.put(self.socket.getsockname())


class VideoStreamingHandler(socketserver.StreamRequestHandler):
    """Request Handler for handling video streaming"""

    def __init__(self, request, client_address, server):
        # self.wbufsize = 3072000
        self.framerate = 30
        super().__init__(request, client_address, server)

    @property
    def delay(self) -> float:
        return 1 / self.framerate

    def handle(self):

        # if self.client_address not in self.server.first:
        #     self.server.first[self.client_address] = True
        print("Client connected from {}".format(self.client_address))

        # region Sets up the video streams

        # if self.server.first[self.client_address]:
        #     self.server.first[self.client_address] = False

        depth_stream_info = VideoInitDatagram(self.server.dev, [self.server.stream_type])

        self.wfile.write((depth_stream_info.to_json() + '~~~\n').encode('latin_1'))

        # endregion

        datagram = None
        j = ""
        first = True

        while True:
            self.rfile.readline()
            # print('doing a thing')
            print('waiting for ack')
            start = time.time()
            try:
                data = self.server.cam_q.get()
                if first:
                    first = False

                    # Enables flattening on non-depth images
                    datagram = VideoStreamDatagram(self.server.dev, self.server.stream_type.name, data,
                                                   self.server.stream_type.dtype,
                                                   self.server.stream_type.dtype != VideoStreamType.Z16)
                else:
                    datagram.frame = data

                j = datagram.to_json()
                print('sending data')
                self.wfile.write((j + '~~~\n').encode('latin-1'))
            except Exception as e:
                print(e)
                # break

            # # Ensures at max, 30 fps
            # elapsed = time.time() - start
            # if elapsed < self.delay:
            #     diff = self.delay - elapsed
            #     time.sleep(diff)

            elapsed = time.time() - start

            self.server.fps = (1 / elapsed) if elapsed != 0 else np.inf

            if self.server.tx_q is not None:
                self.server.tx_q.put(self.server.fps)

        self.server.fps = 0
        if self.server.tx_q is not None:
            self.server.tx_q.put(self.server.fps)
