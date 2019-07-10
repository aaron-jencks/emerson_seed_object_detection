import cython
from cpython cimport array
import array
cimport numpy as np
import numpy as np


@cython.boundscheck(False)
cpdef depth_to_bytes(unsigned short[:, :] depth_image):
    cdef int i, j, index = 0, height = depth_image.shape[0], width = depth_image.shape[1]
    cdef unsigned short current
    cdef unsigned char[:] result = np.zeros(shape=height * width * 2, dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            current = depth_image[i, j]
            result[index] = current & 0xFF
            result[index + 1] = current >> 8
            index = index + 2

    return np.asarray(result)


cpdef bytes_to_depth(bytes depth_bytes, int dtype, int height, int width):
    cdef unsigned short[:] darr
    cdef double[:] dtarr
    cdef double[:, :] drearr
    cdef unsigned char[:] arr
    cdef unsigned char[:, :] grearr
    cdef unsigned char[:, :, :] rearr

    if dtype == 2:
        darr = np.asarray(array.array('H', depth_bytes))
        dtarr = np.multiply(darr, 1 / np.asarray(darr).max())
        drearr = np.reshape(dtarr, (height, width))
        return np.rot90(np.asarray(drearr))
    elif dtype == 1:
        arr = np.asarray(array.array('B', depth_bytes))
        grearr = np.reshape(arr, (height, width))
        return np.rot90(np.asarray(grearr))
    else:
        arr = np.asarray(array.array('B', depth_bytes))
        rearr = np.reshape(arr, (height, width, -1))
        return np.rot90(np.asarray(rearr))


@cython.boundscheck(False)
cpdef convert_realsense(object frames, double scale):
    cdef unsigned char[:, :, :] rgb_frame = np.asanyarray(frames.get_color_frame().get_data(), dtype=np.uint8)
    cdef unsigned char[:, :] ir_frame = np.asanyarray(frames.get_infrared_frame().get_data(), dtype=np.uint8)
    cdef unsigned short[:, :] depth_image = np.asanyarray(frames.get_depth_frame().get_data(), dtype=np.uint16)
    # depth_image = depth_image / depth_image.max()
    
    return np.asarray(rgb_frame), np.asarray(ir_frame), np.asarray(depth_image)
    