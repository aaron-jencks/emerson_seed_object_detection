from PyQt5.QtCore import pyqtSignal

from pmd_implementation.data_structures.state_machine import ThreadedSocketedStateMachine, JMsg
from pmd_implementation.cam_util.cam_ctrl_util import Cam, PMDCam, RealsenseCam


class CamCtrl(ThreadedSocketedStateMachine):
    def __init__(self):
        super().__init__()

        self.pmd = False
        self.cam = None
        self.configuration = {}

        self.states['start_cam'] = self.start_cam
        self.states['reset_cam'] = self.reset_cam
        self.states['configure_cam'] = self.configure_cam
        self.states['start_cap'] = self.start_capture
        self.states['stop_cap'] = self.stop_capture

    def __del__(self):
        if self.cam is not None and self.cam.isConnected:
            if self.cam.isCapturing:
                self.cam.stop_capture()
            self.cam.disconnect()
        self.cam = None

    def find_cam(self):
        """Finds a hardware camera to use, if pmd is True, then finds a pmd camera, otherwise,
        finds a realsense camera"""

        self.cam = PMDCam() if self.pmd else RealsenseCam()
        self.configure_cam()
        self.cam.connect()

    def start_cam(self):
        self.reset_cam()
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
            self.tx.emit(JMsg('frame_update', self.cam.get_frame()))

    def configure_cam(self):

        self.configuration = self.data.data if self.data.data is not None else self.configuration

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
