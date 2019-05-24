import cython
from cython.parallel import prange
from cpython cimport array
import array
cimport numpy as np
import numpy as np
import pyqtgraph as pg
import os


cdef extern from "math.h":
    double sqrt(double x)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef find_formula(double low, double mid, double up):
    cdef double a, b, c
    # TODO Handle zero division

    a = (low / 2 - mid + up / 2) / ((low - mid) * (low - up) * (mid - up))
    b = 0.5 / (mid - low) - a * (low - mid)
    c = 0 - a * low * low - b * low

    return a, b, c


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef create_color_data(double[:, :] depths, double min, double mid, double max):
    cdef double[:, :] colors = np.zeros(shape=(depths.shape[0], 4), dtype=float)

    cdef int c_count = os.cpu_count()

    cdef double r_a, r_b, r_c, g_a, g_b, g_c, b_a, b_b, b_c

    r_a, r_b, r_c = find_formula(max + (max - mid), max, mid)
    g_a, g_b, g_c = find_formula(max, mid, min)
    b_a, b_b, b_c = find_formula(min - (mid - min), min, mid)

    cdef int i
    cdef double z, r, b, g

    for i in prange(depths.shape[0], nogil=True, num_threads=c_count):
        z = depths[i, 2]

        r = r_a * z * z + r_b * z + r_c
        g = g_a * z * z + g_b * z + g_c
        b = b_a * z * z + b_b * z + b_c

        colors[i, 0] = r
        colors[i, 1] = g
        colors[i, 2] = b
        colors[i, 3] = 1

    return np.asarray(colors)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef split_data(double[:, :] frame, int h, int w, int num):

    cdef int row_col_len = int(sqrt(num))
    # print("frame shape is: {}, w is {}, and h is {}".format(frame.shape, w, h))
    cdef int w_inc = w // row_col_len
    cdef int h_inc = h // row_col_len

    cdef double[:, :, :] bits = np.zeros(shape=(num, w_inc, h_inc), dtype=float)
    cdef int c_count = os.cpu_count()
    cdef int i, j, k, ij, ik
    cdef double temp

    for i in prange(num, nogil=True, num_threads=c_count):
        ij = i // row_col_len
        ik = i - row_col_len * ij
        for j in prange(w_inc):
            for k in prange(h_inc):
                # print("Calculating index with parts {} {} {} for a result of {}".format(ij, w_inc, j, ij * w_inc + j))
                temp = frame[ik * h_inc + k, ij * w_inc + j]
                bits[i, j, k] = temp

    return np.asarray(bits)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef concatenate_bits(double[:, :, :] points, long[:] counts):

    cdef int sum = 0, i, j
    cdef int c_count = os.cpu_count()

    for i in prange(points.shape[0], nogil=True, num_threads=c_count):
        sum += counts[i]

    cdef double[:, :] conc = np.zeros(shape=(sum, 3), dtype=float)

    for i in prange(points.shape[0], nogil=True, num_threads=c_count):

        sum = 0
        for j in range(i):
            sum = sum + counts[j]

        for j in range(counts[i]):
            conc[sum - 1 + j, 0] = points[i, j, 0]
            conc[sum - 1 + j, 1] = points[i, j, 1]
            conc[sum - 1 + j, 2] = points[i, j, 2]

    return np.asarray(conc)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef convert_to_points(double[:, :, :] bits, int h, int w, int interpolation):

    cdef int max_num = w * h
    cdef int c_count = os.cpu_count()
    cdef int row_col_len = int(sqrt(c_count))
    cdef int h_inc = h // row_col_len, w_inc = w // row_col_len

    cdef double[:, :, :] points = np.zeros(shape=(c_count, max_num, 3), dtype=float)
    cdef long[:] counts = np.zeros(shape=c_count, dtype=int)

    cdef int count = 0
    cdef int i, r, c, ri, ci, ir, ic, it

    cdef int[:] w_list = array.array('i', range(0, w_inc, interpolation))
    cdef int[:] h_list = array.array('i', range(0, h_inc, interpolation))

    for i in prange(c_count, nogil=True, num_threads=c_count):
        ic = i // row_col_len
        ir = i - row_col_len * ic
        # ic = row_col_len - ic
        count = 0
        for ri in range(h_list.shape[0]):
            r = h_list[ri]
            for ci in range(w_list.shape[0]):
                c = w_list[ci]
                if bits[i, c, r] != 0:
                    # if i == 2 or i == 3:
                    #     print("x is ({} * {}) + {} for {}".format(ic, w_inc, c, (ic * w_inc) + c))
                    #     print("y is ({} * {}) + {} for {}".format(ir, h_inc, r, (ir * h_inc) + r))
                    points[i, count, 0] = (ic * w_inc) + c
                    points[i, count, 1] = (ir * h_inc) + r
                    points[i, count, 2] = bits[i, c, r]
                    count = count + 1
        counts[i] = count

    return np.asarray(points), np.asarray(counts)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef scatter_data(double[:, :] depths, object validator=None,
                         int h=-1, int w=-1, int interpolation=1):

    # Handles if h or w is -1 (default)
    if h < 0 or w < 0:
        h = depths.shape[0] if h < 0 else h
        w = depths.shape[1] if w < 0 else w
        # print("h is {} and w is {}".format(h, w))

    cdef int c_count = os.cpu_count()

    cdef double[:, :, :] bits = split_data(depths, h, w, c_count)
    # print("bits shape is {}".format(bits.shape))

    cdef double[:, :, :] points
    cdef long[:] counts

    points, counts = convert_to_points(bits, h, w, interpolation)

    cdef double[:, :] concatenated = concatenate_bits(points, counts)

    return np.asarray(concatenated)  # , x_cen, y_cen, z_cen
