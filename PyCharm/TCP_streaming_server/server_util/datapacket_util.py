import json
import numpy as np
import io
import base64
import struct
from PIL import Image
import sys
from tqdm import tqdm

from video_util.data import VideoStream, VideoStreamType
import video_util.cy_collection_util as cu


class Datagram:
    """Represents a datagram that can be converted into json and sent across a network connection"""

    def __init__(self, device_identifier: str, gram_type: str):
        self.device = device_identifier
        self.type = gram_type

    def to_json(self) -> str:
        """Converts the contents of this packet into a json string for sending"""
        return json.dumps([self.device, self.type])

    @staticmethod
    def from_json(s: str):
        pass


class VideoInitDatagram(Datagram):
    """Contains information about a Video stream that is about to occur over the current network,
    accepts a list of VideoStream objects from the video_util.data module."""

    def __init__(self, device_identifier: str, streams: list):
        super().__init__(device_identifier, "VideoInit")
        self.streams = streams

    def to_json(self) -> str:
        return json.dumps({'dev': self.device, 'streams': [x.get_dict() for x in self.streams]})

    @staticmethod
    def from_json(s: str):
        j_obj = json.loads(s)
        streams = [VideoStream.from_dict(x) for x in j_obj['streams']]
        return VideoInitDatagram(j_obj['dev'], streams)


class VideoStreamDatagram(Datagram):
    """Contains a single frame from a video stream along with the name that the stream belongs to"""

    def __init__(self, device_identifier: str, name: str, frame: np.ndarray, videotype: VideoStreamType,
                 flatten: bool = False):
        super().__init__(device_identifier, "VideoFrame")
        self.frame = frame.reshape(-1) if flatten else frame
        self.name = name
        self.dtype = videotype

    def to_json(self) -> str:
        b = base64.b64encode(bytes(cu.depth_to_bytes(self.frame) if self.dtype == VideoStreamType.Z16 else self.frame))
        return json.dumps({'dev': self.device, 'name': self.name, 'dtype': self.dtype.value,
                           'frame': b.decode('latin-1')})

    @staticmethod
    def from_json(s: str):
        j_obj = json.loads(s)
        dtype = VideoStreamType(j_obj['dtype'])
        b = base64.b64decode(j_obj['frame'].encode('latin-1'))
        lb = len(b)
        fmt = '{}H'.format(lb//2) if dtype == VideoStreamType.Z16 else '{}B'.format(lb)
        ints = struct.unpack(fmt, b)
        return VideoStreamDatagram(j_obj['dev'], j_obj['name'], np.asarray(ints), dtype)
