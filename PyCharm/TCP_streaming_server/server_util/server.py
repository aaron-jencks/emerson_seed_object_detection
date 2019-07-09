import socketserver
import time

from video_util.cam import Cam
from video_util.data import VideoStreamType, VideoStream
from .datapacket_util import VideoInitDatagram, VideoStreamDatagram


class VideoStreamingServer(socketserver.TCPServer):
    def __init__(self, device_identifier: str, cam: Cam, **kwargs):
        super().__init__(**kwargs)
        self.dev = device_identifier
        self.cam = cam
        self.cam.connect()


class VideoStreamingHandler(socketserver.StreamRequestHandler):
    """Request Handler for handling video streaming"""

    def setup(self):
        super().setup()
        self.server.cam.connect()
        self.server.cam.start_capture()

    def handle(self):

        # region Sets up the video streams

        depth_stream_info = VideoInitDatagram(self.server.dev, [
            VideoStream('rgb', self.server.cam.resolution, self.server.cam.framerate, VideoStreamType.RGB),
            VideoStream('depth', self.server.cam.resolution, self.server.cam.framerate, VideoStreamType.Z16)])

        self.wfile.write((depth_stream_info.to_json() + '\n').encode('utf-8'))

        # endregion

        while True:
            start = time.time()
            try:
                rgb, ir, depth = self.server.cam.get_frame()
                # self.wfile.write((VideoStreamDatagram(self.server.dev, 'rgb', rgb).to_json() + '\n').encode('utf-8'))
                self.wfile.write((VideoStreamDatagram(self.server.dev, 'depth', depth).to_json() + '\n').encode('utf-8'))
            except Exception as e:
                print(e)
                break

            print('\rRunning at {} fps'.format(1 / (time.time() - start)), end='')
        print('')

    def finish(self):
        super().finish()
        self.server.cam.stop_capture()
        self.server.cam.disconnect()
