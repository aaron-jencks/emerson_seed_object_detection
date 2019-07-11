import json
import numpy as np
import io
from PIL import Image
import sys
from tqdm import tqdm
import time

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

    data_separator = '<br>'

    def __init__(self, device_identifier: str, name: str, frame: np.ndarray, videotype: VideoStreamType,
                 flatten: bool = False):
        super().__init__(device_identifier, "VideoFrame")
        self.frame = frame.reshape(-1) if flatten else frame
        self.name = name
        self.dtype = videotype
        self.buff = io.BytesIO()

    def to_json(self) -> str:
        if self.dtype == VideoStreamType.Z16:
            b = bytes(cu.depth_to_bytes(self.frame))
        else:
            if self.dtype == VideoStreamType.RGB:
                md = 'RGB'
            else:
                md = 'L'

            img = Image.fromarray(self.frame, mode=md)
            img.save(self.buff, 'JPEG', quality=30, optimize=True)

            b = bytes(self.buff.getvalue())

        return self.device + self.data_separator + \
            self.name + self.data_separator + \
            self.dtype.name + self.data_separator + b.decode('latin-1')

    @staticmethod
    def from_json(s: str, resolution: tuple = (640, 480)):
        # start = time.time()

        j_obj = s.split(VideoStreamDatagram.data_separator)
        dtype = VideoStreamType[j_obj[2]]
        b = j_obj[3].encode('latin-1')

        ints = cu.bytes_to_depth(b, dtype.value, resolution[1], resolution[0])

        # elapsed = time.time() - start
        # print('\rProcessing at {} fps'.format(round((1 / elapsed) if elapsed != 0 else np.inf, 3)), end='')

        return j_obj[0], j_obj[1], ints, dtype
