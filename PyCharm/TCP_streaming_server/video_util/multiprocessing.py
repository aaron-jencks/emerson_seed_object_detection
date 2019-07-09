from multiprocessing import Process, Queue
import time


class CameraServer(Process):
    """Represents a Camera that places it's frames into a Queue object passed in at startup."""

    def __init__(self, cam_type, data_q: Queue, ignore_if_full: bool = True, sleep_if_full: bool = True,
                 filename: str = ""):
        super().__init__()
        self.cam = cam_type
        self.q = data_q
        self.is_stopping = False
        self.ignore = ignore_if_full
        self.sleep = sleep_if_full
        self.filename = filename

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
        self.cam = self.cam(self.filename)
        self.cam.start_streams()
        self.cam.connect()
        self.cam.start_capture()

        try:
            while not self.is_stopping:
                if self.q.full() and self.sleep:
                    time.sleep(1)
                    continue

                frames = self.cam.get_frame()
                self.lossy_put(self.q, frames)
        finally:
            self.cam.stop_capture()
            self.cam.disconnect()


class SplitCamServer(CameraServer):
    """Same as a CameraServer, but accepts 3 Queues and places the rgb, ir, and depth into their own queues"""

    def __init__(self, cam_type, rgb_q: Queue, ir_q: Queue, depth_q: Queue, ignore_if_full: bool = True,
                 sleep_if_full: bool = True, filename: str = ""):
        super().__init__(cam_type, rgb_q, ignore_if_full, sleep_if_full, filename)
        self.cam = cam_type
        self.rgb_q = rgb_q
        self.ir_q = ir_q
        self.depth_q = depth_q

    def run(self) -> None:
        self.cam = self.cam(self.filename)
        self.cam.start_streams()
        self.cam.connect()
        self.cam.start_capture()

        try:
            while not self.is_stopping:
                if (self.rgb_q.full() or self.ir_q.full() or self.depth_q.full()) and self.sleep:
                    time.sleep(1)
                    continue

                rgb, ir, depth = self.cam.get_frame()
                self.lossy_put(self.rgb_q, rgb.tolist())
                self.lossy_put(self.ir_q, ir.tolist())
                self.lossy_put(self.depth_q, depth.tolist())
        finally:
            self.cam.stop_capture()
            self.cam.disconnect()
