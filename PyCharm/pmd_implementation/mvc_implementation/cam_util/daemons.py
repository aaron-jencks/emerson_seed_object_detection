from PyQt5.QtCore import pyqtSignal

from mvc_implementation.data_structures.state_machine import ThreadedSocketedStateMachine, JMsg
from mvc_implementation.cam_util.cam_ctrl_util import PMDCam, RealsenseCam

import multiprocessing as mp
import time


class CamCtrl(ThreadedSocketedStateMachine):
    def __init__(self, tx_q: mp.Queue, rx_q: mp.Queue, parent=None):
        super().__init__(tx_q, rx_q, parent)

        self.pmd = True
        self.cam = None
        self.configuration = {}
        self.resolution = None
        self.file = ""

        self.states['start_cam'] = self.start_cam
        self.states['reset_cam'] = self.reset_cam
        self.states['configure_cam'] = self.configure_cam
        self.states['start_cap'] = self.start_capture
        self.states['stop_cap'] = self.stop_capture
        self.states['filename'] = self.update_filename

    def __del__(self):
        self.cam.halt = True
        if self.cam is not None and self.cam.isConnected:
            if self.cam.isCapturing:
                self.cam.stop_capture()
            self.cam.disconnect()
        self.cam = None

    @property
    def width(self):
        return self.resolution[0] if self.resolution is not None else -1

    @property
    def height(self):
        return self.resolution[1] if self.resolution is not None else -1

    def update_filename(self, data: str):
        self.file = data

    def find_cam(self):
        """Finds a hardware camera to use, if pmd is True, then finds a pmd camera, otherwise,
        finds a realsense camera"""

        self.cam = PMDCam(file=self.file, disp_parent=self.parent) if self.pmd else RealsenseCam(disp_parent=self.parent)
        self.configure_cam()
        self.cam.connect()
        self.resolution = self.cam.resolution

    def start_cam(self):
        if self.cam is None or not self.cam.isConnected:
            self.find_cam()
        self.start_capture()

    def reset_cam(self):
        """Resets the connections to the hardware camera, and finds it again, used when pmd is toggled."""
        if self.cam is not None and self.cam.isConnected:
            if self.cam.isCapturing:
                self.cam.stop_capture()
            self.cam.disconnect()
        self.find_cam()

    def idle_state(self):

        # Collects and sends off a frame if there isn't anything else the daemon needs to do
        if self.cam is not None and self.cam.isCapturing:
            frames = self.cam.get_frame()
            if frames is not None:
                self.tx.put(JMsg('frame_update', frames))
        else:
            time.sleep(0.5)

    def configure_cam(self, data):
        if not self.pmd:
            self.configuration = data if data is not None else self.configuration

            self.__configure_cam()

    def __configure_cam(self):

        if self.cam is not None:
            configs = self.cam.get_configure_states()
            for k in self.configuration.keys():
                if k in configs:
                    configs[k](**self.configuration[k])

    def start_capture(self):
        if self.cam is not None and not self.cam.isCapturing:
            if not self.cam.isConnected:
                self.cam.connect()

            self.cam.start_capture()

    def stop_capture(self):
        if self.cam is not None and self.cam.isCapturing:
            self.cam.stop_capture()
