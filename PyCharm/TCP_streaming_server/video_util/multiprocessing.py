from multiprocessing import Process, Queue
import time
import numpy as np


class CameraServer(Process):
    """Represents a Camera that places it's frames into a Queue object passed in at startup."""

    def __init__(self, cam_type, data_q: Queue, tx_q: Queue = None,
                 ignore_if_full: bool = True, sleep_if_full: bool = True,
                 filename: str = "", configuration_file: str = ""):
        super().__init__()
        self.cam = cam_type
        self.q = data_q
        self.tx_q = tx_q
        self.is_stopping = False
        self.ignore = ignore_if_full
        self.sleep = sleep_if_full
        self.filename = filename
        self.settings = configuration_file

    def join(self, **kwargs):
        """Stops the camera server"""
        self.is_stopping = True
        super().join(**kwargs)

    def lossy_put(self, q, data):
        if q is not None:
            if not self.ignore:
                while q.full():
                    q.get()

                q.put(data)
            elif not q.full():
                q.put(data)

    def run(self) -> None:
        self.cam = self.cam(self.filename, self.settings)
        self.cam.start_streams()
        self.cam.connect()
        self.cam.start_capture()

        try:
            while not self.is_stopping:
                if self.q.full() and self.sleep:
                    time.sleep(1)
                    continue
                elif self.q.full():
                    print('Purging queue')
                    while not self.q.empty():
                        try:
                            self.q.get_nowait()
                        finally:
                            break

                frames = self.cam.get_frame()
                self.lossy_put(self.q, frames)
        finally:
            self.cam.stop_capture()
            self.cam.disconnect()


class SplitCamServer(CameraServer):
    """Same as a CameraServer, but accepts 3 Queues and places the rgb, ir, and depth into their own queues"""

    def __init__(self, cam_type, rgb_q: Queue = None, ir_q: Queue = None, depth_q: Queue = None, tx_q: Queue = None,
                 ignore_if_full: bool = True, sleep_if_full: bool = False,
                 filename: str = "", configuration_file: str = ""):
        super().__init__(cam_type, rgb_q, tx_q, ignore_if_full, sleep_if_full, filename, configuration_file)
        self.cam = cam_type
        self.rgb_q = rgb_q
        self.ir_q = ir_q
        self.depth_q = depth_q
        self.fps = 0
        print("Creating split camera server")

    def run(self) -> None:
        self.cam = self.cam(self.filename)

        self.cam.set_framerate(90)
        self.cam.set_resolution(640, 480)
        self.cam.start_depth_stream()

        self.cam.set_framerate(90)
        self.cam.set_resolution(640, 480)
        self.cam.start_ir_stream()

        self.cam.set_framerate(30)
        self.cam.set_resolution(1280, 720)
        self.cam.start_color_stream()

        # self.cam.start_streams()
        self.cam.connect()
        self.cam.start_capture()

        try:
            while not self.is_stopping:
                if (
                        (self.rgb_q is not None and self.rgb_q.full()) or
                        (self.ir_q is not None and self.ir_q.full()) or
                        (self.depth_q is not None and self.depth_q.full())
                   ) and self.sleep:
                    time.sleep(1)
                    continue
                elif (self.rgb_q is not None and self.rgb_q.full()) or \
                        (self.ir_q is not None and self.ir_q.full()) or \
                        (self.depth_q is not None and self.depth_q.full()):
                    if self.rgb_q is not None:
                        while not self.rgb_q.empty():
                            try:
                                self.rgb_q.get_nowait()
                            finally:
                                break
                    if self.ir_q is not None:
                        while not self.ir_q.empty():
                            try:
                                self.ir_q.get_nowait()
                            finally:
                                break
                    if self.depth_q is not None:
                        while not self.depth_q.empty():
                            try:
                                self.depth_q.get_nowait()
                            finally:
                                break

                start = time.time()
                rgb, ir, depth = self.cam.get_frame()
                self.lossy_put(self.rgb_q, rgb.reshape(-1))
                self.lossy_put(self.ir_q, ir.reshape(-1))
                self.lossy_put(self.depth_q, depth)
                elapsed = time.time() - start
                self.fps = (1 / elapsed) if elapsed != 0 else np.inf

                if self.tx_q is not None:
                    self.tx_q.put(self.fps)
        finally:
            self.cam.stop_capture()
            self.cam.disconnect()
