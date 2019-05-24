import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np


@cython.boundscheck(False)
cpdef double[:, :] threshold_fast(int T, double[:, :] image):
    # set the variable extension types
    cdef int x, y, w, h

    # grab the image dimensions
    h = image.shape[0]
    w = image.shape[1]

    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            image[y, x] = 255 if image[y, x] >= T else 0

    # return the thresholded image
    return image


@cython.boundscheck(False)
cpdef scatter_data(double[:, :] depths, object validator=None,
                         int h=-1, int w=-1, int interpolation=10):
    # Handles if h or w is -1 (default)
    if h < 0 or w < 0:
        h = depths.shape[0] if h < 0 else h
        w = depths.shape[1] if w < 0 else w

    cdef array.array x = array.array('i', [])
    cdef array.array y = array.array('i', [])
    cdef array.array z = array.array('d', [])
    
    max_num = w * h
    
    array.resize(x, max_num)
    array.resize(y, max_num)
    array.resize(z, max_num)
    
    cdef int count = 0
    cdef int r, c

    # filters the depth image for only valid points and those that have depths > 0
    for r in range(0, w, interpolation):
        for c in range(0, h, interpolation):
            if (validator(r, c) if validator is not None else True) and depths[c][r] != 0:
                x[count] = w - r
                y[count] = c
                z[count] = depths[c][r]
                count += 1
                
    array.resize(x, count)
    array.resize(y, count)
    array.resize(z, count)

    return x, y, z