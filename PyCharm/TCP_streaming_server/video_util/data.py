from enum import Enum


class VideoStreamType(Enum):
    RGB = 0
    Z16 = 1


class VideoStream:
    """Contains data about the properties of a video stream"""

    def __init__(self, name: str, resolution: tuple, framerate: int, dtype: VideoStreamType):
        self.name = name
        self.resolution = resolution
        self.fps = framerate
        self.dtype = dtype

    def get_dict(self) -> dict:
        """Returns this object as a dictionary"""
        return {'name': self.name, 'resolution': self.resolution, 'fps': self.fps, 'dtype': self.dtype.value}

    @staticmethod
    def from_dict(d: dict):
        """Creates an instance of this class from a dictionary"""
        return VideoStream(d['name'], d['resolution'], d['fps'], d['dtype'])
