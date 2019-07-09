import pyrealsense2 as rs

import video_util.cy_collection_util as cu


class Cam:
    def __init__(self, filename: str = ""):
        self.cap = None
        self.isConnected = False
        self.isCapturing = False
        self.halt = False  # Used for looping while repeatedly trying to connect to the camera
        self.resolution = None
        self.file = filename

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
    def __init__(self, filename: str = ""):
        super().__init__(filename)

        self.pipeline = rs.pipeline(rs.context())
        self.config = rs.config()
        self.resolution = (640, 480)
        self.framerate = 90

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
                print(e)
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
        self.__start_stream(rs.stream.color, self.resolution, rs.format.y8, self.framerate)

    def start_depth_stream(self):
        self.__start_stream(rs.stream.depth, self.resolution, rs.format.z16, self.framerate)

    def start_streams(self):
        self.config.enable_all_streams()
