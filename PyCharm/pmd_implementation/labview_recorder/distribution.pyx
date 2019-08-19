import cython
from cython.parallel import prange

cimport numpy as np
import numpy as np

import struct


cdef extern from "math.h":
    double sqrt(double x)


cpdef compute_depth_bytes(unsigned short[:, :] data):
    cdef int i, j, height = data.shape[0], width = data.shape[1]
    cdef unsigned short current
    cdef unsigned char[:] current_bytes

    cdef unsigned char[:, :, :] result = np.ones(shape=(height, width, 3), dtype=np.uint8)

    for i in range(height):
        for j in range(width):
            current = data[i, j]
            # current_bytes = struct.pack('H', current)
            result[i, j, 0] = current & 0xFF
            result[i, j, 1] = current >> 8
            # result[i, j, 0] = current_bytes[0]
            # result[i, j, 1] = current_bytes[1]

    return np.asarray(result)


@cython.boundscheck(False)
cpdef normal_distribution(object frames):
    """Calculates the standard deviation for this population"""

    cdef double[:, :] depth_image = np.multiply(np.asanyarray(frames.get_depth_frame().get_data()), 1).astype(float)

    cdef int i, j, ij, height = depth_image.shape[0], width = depth_image.shape[1]
    cdef double mew_sum = 0, count = 0

    for i in prange(height, nogil=True):
        for j in range(width):
            mew_sum += depth_image[i, j]
            count += 1

    cdef double std_dev, dev_sum = 0, dev_temp
    cdef double avg = mew_sum / count

    # Calculates the standard deviation
    for i in prange(height, nogil=True):
        for j in range(width):
            dev_temp = depth_image[i, j] - avg
            dev_sum += dev_temp * dev_temp

    std_dev = sqrt(dev_sum / count)

    # Calculates the z-values
    cdef double[:] result = np.zeros(shape=int(count), dtype=float)

    for i in prange(height, nogil=True):
        for j in range(width):
            ij = i * width + j

            if std_dev != 0:
                result[ij] = ((depth_image[i, j] - avg) / std_dev)
            else:
                result[ij] = 0

    return result