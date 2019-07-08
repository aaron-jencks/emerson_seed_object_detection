import json
import numpy as np


class Datagram:
    """Represents a datagram that can be converted into json and sent across a network connection"""

    def __init__(self, device_identifier: str, gram_type: str):
        self.device = device_identifier
        self.type = gram_type

    def to_json(self) -> str:
        """Converts the contents of this packet into a json string for sending"""
        return json.dumps([self.device, self.type])


class VideoInitDatagram(Datagram):
    """Contains information about a Video stream that is about to occur over the current network,
    accepts a list of VideoStream objects from the video_util.data module."""

    def __init__(self, device_identifier: str, streams: list):
        super().__init__(device_identifier, "VideoInit")
        self.streams = streams

    def to_json(self) -> str:
        return json.dumps({'dev': self.device, 'streams': [x.get_dict() for x in self.streams]})


class VideoStreamDatagram(Datagram):
    """Contains a single frame from a video stream along with the name that the stream belongs to"""

    def __init__(self, device_identifier: str, name: str, frame: np.ndarray):
        super().__init__(device_identifier, "VideoFrame")
        self.frame = frame.reshape(shape=-1)
        self.name = name

    def to_json(self) -> str:
        return json.dumps({'dev': self.device, 'name': self.name, 'frame': self.frame.tolist()})
