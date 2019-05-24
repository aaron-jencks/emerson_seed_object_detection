import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np
import cv2


@cython.boundscheck(False)
cpdef convert_realsense(object frames, double scale):
    frame = np.asanyarray(frames.get_infrared_frame().get_data())
    depth_image = cv2.convertScaleAbs(np.asanyarray(frames.get_depth_frame().get_data()), alpha=scale)
    depth_image = depth_image / depth_image.max()
    
    return frame, depth_image


@cython.boundscheck(False)
cpdef convert_array(int[:] values, int size):
    cdef int[:] n_arr = np.asarray(values)
    return n_arr.reshape(-1, size)


@cython.boundscheck(False)
cpdef convert_gray(object data):
    cdef int r = data.getNumPoints()
    cdef int[:] r_rng = array.array('i', range(r))
    
    cdef int[:] g_val = array.array('i', r_rng)
    
    cdef int i
    for i in r_rng:
        g_val[i] = data.getGrayValue(i)
        
    return cv2.convertScaleAbs(convert_array(g_val, data.width))

@cython.boundscheck(False)
cpdef convert_raw(object data):
    cdef int r = data.getNumPoints()
    cdef int[:] r_rng = array.array('i', range(r))
    
    cdef int[:] z_val = array.array('i', r_rng)
    cdef int[:] g_val = array.array('i', r_rng)
    
    cdef int i
    for i in r_rng:
        z_val[i] = data.getZ(i)
        g_val[i] = data.getGrayValue(i)
        
    return convert_array(z_val, data.width), cv2.convertScaleAbs(convert_array(g_val, data.width))
    