import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np


@cython.boundscheck(False)
cpdef convert_realsense(object frames, double scale):
    frame = np.rot90(np.asanyarray(frames.get_infrared_frame().get_data()))
    cdef double[:, :] depth_image = np.multiply(np.asanyarray(frames.get_depth_frame().get_data()), scale)
    # depth_image = depth_image / depth_image.max()
    
    return frame, np.asarray(depth_image)
    