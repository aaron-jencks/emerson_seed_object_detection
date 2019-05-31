import cython
from cython.parallel import prange
from cpython cimport array
import array
cimport numpy as np
import numpy as np
import pyqtgraph as pg
import os

from mvc_implementation.data_structures.sorting cimport heapsort


cdef extern from "math.h":
    double sqrt(double x)


cdef int c_count = os.cpu_count()
cdef int c_count_square = int(sqrt(c_count))


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef get_roi_coords_matrix(int height, int width):

    cdef int length = height * width

    cdef double[:, :, :] xys = np.zeros(shape=(height, width, 2), dtype=float)

    cdef int i, j

    for i in prange(height, nogil=True, num_threads=c_count_square):
        for j in prange(width, num_threads=c_count_square):
            xys[i, j, 0] = i
            xys[i, j, 1] = j

    return np.asarray(xys, dtype=float)


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef apply_roi(double[:, :] depths, double[:, :, :] roi_coords):

    cdef int h = roi_coords.shape[0], w = roi_coords.shape[1]
    cdef int i, j, ii, ij, length = h * w
    cdef int x, y

    cdef double[:, :] points = np.zeros(shape=(length, 3), dtype=float)

    for i in prange(h, nogil=True, num_threads=c_count_square):
        ii = i * w
        for j in prange(w, num_threads=c_count_square):
            ij = ii + j
            x = int(roi_coords[i, j, 1])
            y = int(roi_coords[i, j, 0])
            if depths[x, y] > 0:
                points[ij, 0] = x
                points[ij, 1] = y
                points[ij, 2] = depths[x, y]

    return np.asarray(points)


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef average_depth(double[:, :] coordinates):
    cdef double sum = 0, current = 0, mn = 1000, mx = 0
    cdef int count = 0, i
    cdef int length = coordinates.shape[0]

    cdef double[:] depths = np.zeros(shape=length, dtype=float)

    for i in range(length):  # , nogil=True, num_threads=c_count):
        current = coordinates[i, 2]

        if current < mn:
            mn = current
        if current > mx:
            mx = current

        sum += current
        count += 1

    if count > 0:
        # heapsort(depths)  # Puts them in order so that we can just pull the min/max out of the 0th and last elements
        return sum / float(count), mn, mx
    else:
        return 0, 0, 0


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef apply_depth_scale(double[:, :] coordinates, double scale):

    cdef double[:, :] temp_depths
    cdef int i, j, int_scale = int(scale)
    cdef int r = coordinates.shape[0]
    cdef double actual_scale = scale

    if coordinates.shape[0] > 0:
        # print(coordinates.shape)
        temp_depths = np.zeros(shape=(coordinates.shape[0], coordinates.shape[1]), dtype=float)

        # for i in prange(int_scale, nogil=True, num_threads=c_count):
        #     actual_scale *= 10

        for i in prange(r, nogil=True, num_threads=c_count):
            for j in range(2):
                temp_depths[i, j] = coordinates[i, j]
            temp_depths[i, 2] = coordinates[i, 2] * actual_scale

        return np.asarray(temp_depths)
    else:
        return coordinates


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef create_color_depth_image(double[:, :] coordinates, double[:, :] colors, int image_height, int image_width):
    cdef double[:, :, :] depth_image = np.zeros(shape=(image_height, image_width, 3), dtype=float)
    cdef int i, j, k

    cdef int num_coords = coordinates.shape[0]
    cdef int x, y

    for i in prange(num_coords, nogil=True, num_threads=c_count):
        x = int(coordinates[i, 0])
        y = int(coordinates[i, 1])

        for j in range(3):
            depth_image[y, x, j] = colors[i, j]

    return np.asarray(depth_image)


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef find_formula(double low, double mid, double up):
    cdef double a, b, c
    cdef double x1_1, x2_1, x1_2, x2_2, x1_3, x2_3, x1_4, x2_4, x1_5, x2_5, x1_6
    cdef double y1, y2, y3, y4, y5, y6
    # TODO Handle zero division

    x1_1 = low * low
    x2_1 = low

    x1_2 = mid * mid
    x2_2 = mid

    x1_3 = up * up
    x2_3 = up

    x1_4 = x1_1 - x1_2
    x2_4 = x2_1 - x2_2

    x1_5 = x1_3 - x1_2
    x2_5 = x2_3 - x2_2

    x1_6 = x1_4 * x2_5 - x1_5 * x2_4
    y6 = x2_4 - x2_5

    # y6 = x1_6 * a
    a = y6 / x1_6

    # y5 = x1_5 * a + x2_5 * b
    b = (-1 - x1_5 * a) / x2_5

    # y1 = x1_1 * a + x2_1 * b + c
    c = 0 - (x1_1 * a + x2_1 * b)

    return a, b, c


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef create_color_data(double[:, :] depths, double min, double mid, double max):
    cdef double[:, :] colors = np.zeros(shape=(depths.shape[0], 4), dtype=float)

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

        colors[i, 0] = r if z < max and 0 <= r <= 1 else 0 if z < max and r < 0 else 1
        colors[i, 1] = g if min < z < max and 0 <= g <= 1 else 0
        colors[i, 2] = b if z > min and 0 <= b <= 1 else 0 if z > min and b < 0 else 1
        colors[i, 3] = 1

    return np.asarray(colors)


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef scatter_data(double[:, :] depths, object validator=None,
                         int h=-1, int w=-1, int interpolation=1):

    # Handles if h or w is -1 (default)
    if h < 0 or w < 0:
        h = depths.shape[0] if h < 0 else h
        w = depths.shape[1] if w < 0 else w
        # print("h is {} and w is {}".format(h, w))

    cdef double[:, :] points = np.zeros(shape=(h * w, 3), dtype=float)
    cdef int count = 0

    cdef int i, j, k, ii, ij

    for i in prange(h, nogil=True, num_threads=c_count_square):
        ii = i * w
        for j in prange(w, num_threads=c_count_square):
            if depths[i, j] > 0:
                ij = ii + j
                points[ij, 0] = j
                points[ij, 1] = i
                points[ij, 2] = depths[i, j]
                count += 1

    points = np.resize(points, (count, 3))

    return np.asarray(points)
