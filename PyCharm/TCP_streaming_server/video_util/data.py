from enum import Enum


class VideoStreamType(Enum):
    RGB = 0
    GRAY = 1
    Z16 = 2


class VideoStream:
    """Contains data about the properties of a video stream"""

    def __init__(self, name: str, resolution: tuple, framerate: int, dtype: VideoStreamType, depth_scale: float = 1):
        self.name = name
        self.resolution = resolution
        self.fps = framerate
        self.dtype = dtype
        self.scale = depth_scale

    def get_dict(self) -> dict:
        """Returns this object as a dictionary"""
        return {'name': self.name, 'resolution': self.resolution, 'fps': self.fps, 'dtype': self.dtype.value,
                'scale': self.scale}

    @staticmethod
    def from_dict(d: dict):
        """Creates an instance of this class from a dictionary"""
        return VideoStream(d['name'], d['resolution'], d['fps'], d['dtype'], d['scale'])
