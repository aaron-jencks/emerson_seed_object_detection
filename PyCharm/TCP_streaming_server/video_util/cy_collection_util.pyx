import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np


@cython.boundscheck(False)
cpdef convert_realsense(object frames, double scale):
    rgb_frame = np.asanyarray(frames.get_color_frame().get_data())
    ir_frame = np.asanyarray(frames.get_infrared_frame().get_data())
    cdef double[:, :] depth_image = np.multiply(np.asanyarray(frames.get_depth_frame().get_data()), scale)
    # depth_image = depth_image / depth_image.max()
    
    return np.asarray(rgb_frame), np.asarray(ir_frame), np.asarray(depth_image)
    