from multiprocessing import Process, Queue

from .cam import Cam


class CameraServer(Process):
    """Represents a Camera that places it's frames into a Queue object passed in at startup."""

    def __init__(self, cam: Cam, data_q: Queue):
        super().__init__()
        self.cam = cam
        self.q = data_q
        self.is_stopping = False

    def join(self, **kwargs):
        """Stops the camera server"""
        self.is_stopping = True
        super().join(**kwargs)

    def run(self) -> None:
        self.cam.connect()
        self.cam.start_capture()

        while not self.is_stopping:
            frames = self.cam.get_frame()
            self.q.put(frames)

        self.cam.stop_capture()
        self.cam.disconnect()
