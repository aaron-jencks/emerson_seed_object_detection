import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np
import cv2

from tqdm import tqdm


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
cpdef convert_roi(long l, long u, long r, long b, long width):
    """Converts the roi array tuples into a series of ranges that can be used for extracting data from the image"""
    cdef long h = b - u + 1, w = r - l + 1, start_index = u * width + l

    cdef long[:] result = np.zeros(shape=h * w, dtype=int)

    cdef int i, j, ii, s_temp
    for i in range(h):
        ii = i * w
        s_temp = start_index + i * width
        for j in range(w):
            result[ii + j] = s_temp + j

    return np.asarray(result, dtype=int)

@cython.boundscheck(False)
cpdef convert_raw(int[:] roi, np.ndarray data, int width):
    # print("Getting number of points")
    cdef int r = data.shape[0]

    if roi.shape[0] > 0:
        r = roi.shape[0]
    
    cdef double[:] z_val = np.zeros(shape=r, dtype=float)
    cdef long[:] g_val = np.zeros(shape=r, dtype=int)

    # print("Collecting data")
    cdef int i
    for i in range(r):
        if roi.shape[0] > 0:
            z_val[i] = data[roi[i]].z
            g_val[i] = data[roi[i]].grayValue
        else:
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
    