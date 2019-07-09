from multiprocessing import Process, Queue

from .cam import Cam


class CameraServer(Process):
    """Represents a Camera that places it's frames into a Queue object passed in at startup."""

    def __init__(self, cam: Cam, data_q: Queue, ignore_if_full: bool = True):
        super().__init__()
        self.cam = cam
        self.q = data_q
        self.is_stopping = False
        self.ignore = ignore_if_full

    def join(self, **kwargs):
        """Stops the camera server"""
        self.is_stopping = True
        super().join(**kwargs)

    def lossy_put(self, q: Queue, data):
        if not self.ignore:
            while q.full():
                q.get()

            q.put(data)
        elif not q.full():
            q.put(data)

    def run(self) -> None:
        self.cam.connect()
        self.cam.start_capture()

        while not self.is_stopping:
            frames = self.cam.get_frame()
            self.lossy_put(self.q, frames)

        self.cam.stop_capture()
        self.cam.disconnect()


class SplitCamServer(CameraServer):
    """Same as a CameraServer, but accepts 3 Queues and places the rgb, ir, and depth into their own queues"""

    def __init__(self, cam: Cam, rgb_q: Queue, ir_q: Queue, depth_q: Queue, ignore_if_full: bool = True):
        super().__init__(cam, rgb_q, ignore_if_full)
        self.cam = cam
        self.rgb_q = rgb_q
        self.ir_q = ir_q
        self.depth_q = depth_q

    def run(self) -> None:
        self.cam.connect()
        self.cam.start_capture()

        while not self.is_stopping:
            rgb, ir, depth = self.cam.get_frame()
            self.lossy_put(self.rgb_q, rgb)
            self.lossy_put(self.ir_q, ir)
            self.lossy_put(self.depth_q, depth)

        self.cam.stop_capture()
        self.cam.disconnect()
