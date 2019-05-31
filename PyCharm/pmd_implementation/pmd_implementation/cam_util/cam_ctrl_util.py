import numpy as np
import pyximport; pyximport.install(setup_args={"include_dirs":np.get_include()})
import pmd_implementation.cam_util.cy_collection_util as cu

import pyrealsense2 as rs

import roypy
import roypy_platform_utils
import roypy_sample_utils
import sample_camera_info
import argparse

from collections import deque
from queue import Queue

import sys
import traceback
from pmd_implementation.dependencies.display_util.string_display_util import print_warning

import time


class Cam:
    def __init__(self):
        self.cap = None
        self.isConnected = False
        self.isCapturing = False
        self.resolution = None

    def connect(self):
        """Connects to the hardware camera"""
        pass

    def disconnect(self):
        """Disconnects from the hardware camera"""
        pass

    def start_capture(self):
        """Enables the ability to collect frames from the camera"""
        pass

    def stop_capture(self):
        """Stops the ability to collect frames from the camera"""
        pass

    def get_frame(self) -> list:
        """Gets the next frame from the camera, returns a list of all available kinds of frames"""
        pass

    def get_configure_states(self):
        """Returns a dictionary of states that can be use to modify the settings of this camera"""
        pass


class RealsenseCam(Cam):
    def __init__(self):
        super().__init__()

        self.pipeline = rs.pipeline(rs.context())
        self.config = rs.config()
        self.resolution = (640, 480)
        self.framerate = 30

    def connect(self):
        if not self.isConnected:
            self.cap = self.pipeline.start(self.config)
            self.isConnected = True

    def disconnect(self):
        if self.isConnected:
            self.pipeline.stop()
            self.cap = None
            self.isConnected = False

    def start_capture(self):
        if not self.isConnected:
            self.connect()
        self.isCapturing = True

    def stop_capture(self):
        if self.isConnected:
            self.disconnect()
        self.isCapturing = False

    @property
    def depth_scale(self):
        return self.cap.get_device().first_depth_sensor().get_depth_scale() if self.cap is not None else -1

    def get_frame(self) -> list:
        if self.isCapturing:
            try:
                frames = self.pipeline.wait_for_frames()
                frame, depth_frame = cu.convert_realsense(frames, self.depth_scale)

                return [frame, depth_frame]
            except RuntimeError as e:
                print("Something went wrong while trying to collect frame for the camera")

    def get_configure_states(self):
        return {'resolution': self.set_resolution, 'framerate': self.set_framerate,
                'ir_stream': self.start_ir_stream, 'depth_stream': self.start_depth_stream}

    def set_framerate(self, fps: int):
        self.framerate = fps

    def set_resolution(self, h: int, w: int):
        self.resolution = (h, w)

    def __start_stream(self, stream: rs.stream, resolution: iter, str_format: rs.format, fps: int):
        """Starts a new stream of the given type, resolution, format, and framerate"""

        # Stops the camera if necessary
        was_capturing = False
        was_connected = False
        if self.isCapturing:
            self.stop_capture()
            was_capturing = True
        if self.isConnected:
            self.disconnect()
            was_connected = True

        self.config.enable_stream(stream, resolution[0], resolution[1], str_format, fps)

        # Reconnects the camera if necessary
        if was_capturing:
            self.start_capture()
        elif was_connected:
            self.connect()

    def start_ir_stream(self):
        self.__start_stream(rs.stream.infrared, self.resolution, rs.format.y8, self.framerate)

    def start_depth_stream(self):
        self.__start_stream(rs.stream.depth, self.resolution, rs.format.z16, self.framerate)


# region Listeners for pmd camera

class ImageListener(roypy.IDepthDataListener):
    def __init__(self, q):
        super(ImageListener, self).__init__()
        self.queue = q

    def onNewData(self, data):
        p = cu.convert_gray(data)
        self.queue.append(p)


class DepthListener(roypy.IDepthDataListener):
    def __init__(self, q, q_depth):
        super(DepthListener, self).__init__()
        self.queue = q_depth
        self.gqueue = q

    def onNewData(self, data):
        try:
            # print("Processing data")
            # zarray = []
            # garray = []
            # for point in tqdm(np.asanyarray(data.points())):
            #     zarray.append(point.z)
            #     garray.append(point.grayValue)
            # garray = np.rot90(np.asarray(cv2.convertScaleAbs(np.asarray(garray).reshape(-1, data.width))))
            # zarray = np.asarray(zarray, dtype=float).reshape(-1, data.width)
            zarray, garray = cu.convert_raw(np.asanyarray(data.points()), data.width)
            # print("Appending data")
            self.queue.append(zarray)
            self.gqueue.append(garray)
        except Exception as e:
            et, ev, tb = sys.exc_info()
            exc = "Exception was thrown: {}\n".format(e)
            for l in traceback.format_exception(et, ev, tb):
                exc += l
            exc += '\nExitting...'
            print_warning(exc)

# endregion


class PMDCam(Cam):
    def __init__(self, file: str = ""):
        super().__init__()

        self.platform = roypy_platform_utils.PlatformHelper()

        self.file = file

        parser = argparse.ArgumentParser()
        roypy_sample_utils.add_camera_opener_options(parser)
        self.options = parser.parse_args("")

        self.manager = roypy_sample_utils.CameraOpener(self.options)
        self.frame_q = deque()
        self.depth_q = deque()
        self.listener = DepthListener(self.frame_q, self.depth_q)
        self.exposure = 80
        self.mode = 'MODE_5_45FPS_500'

    # region Built-ins

    def connect(self):

        if self.file == "":
            self.cap = self.manager.open_camera()
            self.cap.setUseCase(self.mode)
            self.cap.setExposureTime(self.exposure)
            sample_camera_info.print_camera_info(self.cap)
            print("isConnected", self.cap.isConnected())
            print("getFrameRate", self.cap.getFrameRate())
        else:
            self.cap = self.manager.open_recording(self.file)

        self.cap.registerDataListener(self.listener)
        self.isConnected = True

    def disconnect(self):
        self.cap.unregisterDataListener()
        self.cap = None
        self.isConnected = False

    def start_capture(self):
        if self.isConnected and not self.isCapturing:
            self.cap.startCapture()
            self.isCapturing = True

    def stop_capture(self):
        if self.isCapturing:
            self.cap.stopCapture()
            self.isCapturing = False

    def get_frame(self) -> list:
        if len(self.depth_q) > 0 and len(self.frame_q) > 0:
            frame = self.frame_q.popleft()
            depth = self.depth_q.popleft()

            if len(self.depth_q) > 10 or len(self.frame_q) > 10:
                self.flush_queues()

            return [frame, depth]
        else:
            time.sleep(0.1)

    def get_configure_states(self):
        return {'mode': self.set_mode, 'exposure': self.set_exposure}

    # endregion

    def set_exposure(self, exp: int):
        self.exposure = exp

        # Changes the current camera if necessary
        if self.isConnected:
            self.cap.setExposureTime(self.exposure)

    def set_mode(self, mode: str):
        self.mode = mode

        # Changes the current camera if necessary
        if self.isConnected:
            self.cap.setUseCase(self.mode)

    def flush_queues(self):
        self.frame_q.clear()
        self.depth_q.clear()
