import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np
import cv2

from tqdm import tqdm

@cython.boundscheck(False)
cpdef convert_realsense(object frames, double scale):
    frame = np.rot90(np.asanyarray(frames.get_infrared_frame().get_data()))
    cdef double[:, :] depth_image = np.multiply(np.asanyarray(frames.get_depth_frame().get_data()), scale)
    # depth_image = depth_image / depth_image.max()
    
    return frame, np.asarray(depth_image)


@cython.boundscheck(False)
cpdef convert_array(int[:] values, int size):
    cdef np.ndarray n_arr = np.asarray(values)
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
cpdef convert_raw(np.ndarray data, int width):
    # print("Getting number of points")
    cdef int r = data.shape[0]
    
    cdef double[:] z_val = np.zeros(shape=r, dtype=float)
    cdef long[:] g_val = np.zeros(shape=r, dtype=int)

    # print("Collecting data")
    cdef int i
    for i in range(r):
        z_val[i] = data[i].z
        g_val[i] = data[i].grayValue

    # print("Processing the data")

    cdef np.ndarray img = np.asarray(cv2.convertScaleAbs(np.asarray(g_val).reshape(-1, width)))
    img = np.rot90(img)

    # print("Returning the data")
    # print(width)
    cdef double[:, :] z_res = np.asarray(z_val, dtype=float).reshape(-1, width)
    # print(z_res.shape[0])
        
    return z_res, img
    