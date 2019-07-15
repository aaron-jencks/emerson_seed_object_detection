from multiprocessing import Queue, Process
from threading import Thread
import time

from ..server import VideoStreamingServer


class ServerStopper(Thread):
    def __init__(self, q: Queue, server: VideoStreamingServer):
        super().__init__()
        self.q = q
        self.server = server

    def run(self) -> None:
        while self.q.empty():
            time.sleep(1)
        self.server.server_close()


class VideoStreamServerWrapper(Process):
    """Wraps a VideoStreamingServer object inside of a process that can be launched on another thread"""

    stop_q = Queue(1)

    def __init__(self, device_identifier: str, cam_q: Queue, tx_q: Queue, **kwargs):
        super().__init__(args=[tx_q])
        self.server = VideoStreamingServer
        self.dev = device_identifier
        self.act_server = None
        self.q = cam_q
        self.tx = tx_q
        self.kwargs = kwargs
        self.name = 'Video Server'

    def join(self, **kwargs) -> None:
        self.stop_q.put(True)
        super().join(**kwargs)

    def run(self) -> None:
        try:
            self.act_server = self.server(self.dev, self.q, tx_q=self.tx, **self.kwargs)

            # Handles stopping the server
            stopper = ServerStopper(self.stop_q, self.act_server)
            stopper.start()

            with self.act_server as server:
                server.serve_forever()
        except Exception as e:
            print(e)
            self.act_server.server_close()
