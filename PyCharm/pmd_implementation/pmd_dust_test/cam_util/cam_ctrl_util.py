import numpy as np
import pmd_dust_test.cam_util.cy_collection_util as cu

import roypy
import roypy_platform_utils
import roypy_sample_utils
import sample_camera_info
import argparse

from collections import deque

import sys
import traceback
from dependencies.display_util.string_display_util import print_warning, print_notification

import time


class Cam:
    def __init__(self, roi: list = None, disp_parent=None, filename: str = ""):
        self.cap = None
        self.isConnected = False
        self.isCapturing = False
        self.halt = False  # Used for looping while repeatedly trying to connect to the camera
        self.resolution = None
        self.file = filename
        self.parent = disp_parent
        self.roi = roi if roi is not None else []

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


# region Listeners for pmd camera

class ImageListener(roypy.IDepthDataListener):
    def __init__(self, q):
        super(ImageListener, self).__init__()
        self.queue = q

    def onNewData(self, data):
        p = cu.convert_gray(data)
        self.queue.append(p)


class DepthListener(roypy.IDepthDataListener):
    def __init__(self, roi: list, q: deque, q_depth: deque):
        super(DepthListener, self).__init__()
        self.roi = roi
        self.converted_roi = None
        self.queue = q_depth
        self.gqueue = q

    def onNewData(self, data):
        try:
            if self.converted_roi is None and len(self.roi) > 0:
                self.converted_roi = cu.convert_roi(self.roi[0], self.roi[1], self.roi[2], self.roi[3], data.width)

            zarray, garray = cu.convert_raw(self.converted_roi, np.asanyarray(data.points()),
                                            (data.width if self.converted_roi is None else
                                            (self.roi[2] - self.roi[0] + 1)))

            self.queue.append(zarray)
            self.gqueue.append(garray)
        except Exception as e:
            et, ev, tb = sys.exc_info()
            exc = "Exception was thrown: {}\n".format(e)
            for l in traceback.format_exception(et, ev, tb):
                exc += l
            print_warning(exc)

# endregion


class PMDCam(Cam):
    def __init__(self, roi: list = None, disp_parent=None, file: str = ""):
        super().__init__(roi, disp_parent, file)

        self.platform = roypy_platform_utils.PlatformHelper()

        parser = argparse.ArgumentParser()
        roypy_sample_utils.add_camera_opener_options(parser)
        self.options = parser.parse_args("")

        self.manager = roypy_sample_utils.CameraOpener(self.options)
        self.frame_q = deque()
        self.depth_q = deque()
        self.listener = DepthListener(self.roi, self.frame_q, self.depth_q)
        self.exposure = 80
        self.mode = 'MODE_5_45FPS_500'

    # region Built-ins

    def connect(self):

        print_notification("Opening camera")

        if self.file == "":
            while not self.halt:
                try:
                    self.cap = self.manager.open_camera()
                    self.cap.setUseCase(self.mode)
                    self.cap.setExposureTime(self.exposure)
                    sample_camera_info.print_camera_info(self.cap)
                    print("isConnected", self.cap.isConnected())
                    print("getFrameRate", self.cap.getFrameRate())
                    break
                except RuntimeError as e:
                    print_warning('Exception was thrown: {}'.format(e))
                    print_notification('Is the camera connected?')
                    input("Press any key to continue")
                    print_notification("Retrying")
        else:
            self.cap = self.manager.open_recording(self.file)

        self.cap.registerDataListener(self.listener)
        self.isConnected = True

    def disconnect(self):
        print_notification("Closing camera")
        self.cap.unregisterDataListener()
        self.cap = None
        self.isConnected = False

    def start_capture(self):
        print_notification("Starting camera")
        if self.isConnected and not self.isCapturing:
            self.cap.startCapture()
            self.isCapturing = True

    def stop_capture(self):
        print_notification("Stopping camera")
        if self.isCapturing:
            self.cap.stopCapture()
            self.isCapturing = False

    def get_frame(self) -> list:
        # print_notification("Getting a frame")
        start = time.time()
        while time.time() - start < 5:
            if len(self.depth_q) > 0 and len(self.frame_q) > 0:
                frame = self.frame_q.popleft()
                depth = self.depth_q.popleft()

                if len(self.depth_q) > 10 or len(self.frame_q) > 10:
                    self.flush_queues()

                return [frame, depth]
            else:
                time.sleep(0.02)
        raise RuntimeError("Frame didn't arrive within 5 seconds")

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
