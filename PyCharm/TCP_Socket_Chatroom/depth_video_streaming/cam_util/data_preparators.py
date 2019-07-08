from depth_video_streaming.data_pickling_util import DataPreparator
import numpy as np
import json


class RealsensePreparator(DataPreparator):
    def __init__(self, rgb_frame: np.ndarray, depth_frame: np.ndarray, depth_scale: float = 0.001, **kwargs):
        super().__init__(**kwargs)
        self.rgb = rgb_frame
        self.depth = depth_frame
        self.scale = depth_scale

    def convert(self, data=None) -> bytes:
        return bytes(json.dumps({'rgb': self.rgb, 'depth': self.depth, 'scale': self.scale}) + '\n', self.encoding)
