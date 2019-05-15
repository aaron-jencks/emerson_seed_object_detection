from roypy_sample_utils import CameraOpener


class CameraOpenerExternTrig(CameraOpener):
    def open_hardware_camera(self):
        """Search for a connected camera and open it, handling the access level.
        """
        c = self._get_camera_manager()
        l = c.getConnectedCameraList()

        print("Number of cameras connected: ", l.size())
        if l.size() == 0:
            raise RuntimeError("No cameras connected")

        cam = c.createCamera(l[0])
        self._pre_initialize(cam)
        cam.setExternalTrigger(True)
        cam.initialize()

        return cam
