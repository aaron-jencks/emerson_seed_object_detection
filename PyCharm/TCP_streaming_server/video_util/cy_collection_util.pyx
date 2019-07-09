import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np


@cython.boundscheck(False)
cpdef convert_realsense(object frames, double scale):
    cdef unsigned char[:, :, :] rgb_frame = np.asanyarray(frames.get_color_frame().get_data(), dtype=np.uint8)
    cdef unsigned char[:, :] ir_frame = np.asanyarray(frames.get_infrared_frame().get_data(), dtype=np.uint8)
    cdef unsigned short[:, :] depth_image = np.asanyarray(frames.get_depth_frame().get_data(), dtype=np.uint16)
    # depth_image = depth_image / depth_image.max()
    
    return np.asarray(rgb_frame), np.asarray(ir_frame), np.asarray(depth_image)
    