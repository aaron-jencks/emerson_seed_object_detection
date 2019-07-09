from multiprocessing import Queue, Process

from ..server import VideoStreamingServer


class VideoStreamServerWrapper(Process):
    """Wraps a VideoStreamingServer object inside of a process that can be launched on another thread"""

    def __init__(self, device_identifier: str, cam_q: Queue, **kwargs):
        super().__init__()
        self.server = VideoStreamingServer
        self.dev = device_identifier
        self.q = cam_q
        self.kwargs = kwargs

    def run(self) -> None:
        with self.server(self.dev, self.q, **self.kwargs) as server:
            server.serve_forever()
