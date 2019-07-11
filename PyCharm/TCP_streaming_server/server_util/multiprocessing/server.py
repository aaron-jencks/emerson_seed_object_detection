from multiprocessing import Queue, Process

from ..server import VideoStreamingServer


class VideoStreamServerWrapper(Process):
    """Wraps a VideoStreamingServer object inside of a process that can be launched on another thread"""

    def __init__(self, device_identifier: str, cam_q: Queue, tx_q: Queue, **kwargs):
        super().__init__(args=[tx_q])
        self.server = VideoStreamingServer
        self.dev = device_identifier
        self.act_server = None
        self.q = cam_q
        self.tx = tx_q
        self.kwargs = kwargs
        self.name = 'Video Server'

    def run(self) -> None:
        self.act_server = self.server(self.dev, self.q, tx_q=self.tx, **self.kwargs)
        with self.act_server as server:
            server.serve_forever()
