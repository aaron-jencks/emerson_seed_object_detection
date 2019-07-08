from depth_video_streaming.cam_util.classes import RealsenseCam
from depth_video_streaming.cam_util.data_preparators import RealsensePreparator
from depth_video_streaming.web_socket_util import get_local_ip
from depth_video_streaming.display_util import print_notification

import socketserver as ss
from collections import deque


class RealsenseDatagramHandler(ss.StreamRequestHandler):

    def handle(self):
        # Start loop for handling stream
        while True:
            # Checks if there was any user input
            if len(self.rfile) > 0:
                command = self.rfile.readline().strip().decode('utf-8')
                if command == "stop":
                    break
                else:
                    pass

            # broadcasts a frame if one is ready
            while len(self.server.frame_buffer) > 0:
                frames = self.server.frame_buffer.popleft()
                preparator = RealsensePreparator(frames[0], frames[1], self.server.cam.depth_scale)
                self.wfile.write(preparator.convert().decode(preparator.encoding))


class CamServer(ss.TCPServer):
    def __init__(self):
        self.host, self.ip = get_local_ip()
        super().__init__((self.host, 0), RealsenseDatagramHandler)
        self.port = self.socket.getsockname()[1]
        self.cam = RealsenseCam()
        print_notification('Created server for {} bound to {} on port {}'.format(self.host, self.ip, self.port))

        self.frame_buffer = deque()
        self.cam.connect()
        self.cam.start_capture()
        print_notification('Started camera capture')

    def service_actions(self):
        super().service_actions()
        self.frame_buffer.append(self.cam.get_frame())


if __name__ == "__main__":
    with CamServer() as server:
        server.serve_forever()
