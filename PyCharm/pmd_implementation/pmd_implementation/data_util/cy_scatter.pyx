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


cdef int c_count = os.cpu_count()
cdef int c_count_square = int(sqrt(c_count))


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef get_roi_coords_matrix(int height, int width):

    cdef int length = height * width

    cdef double[:, :, :] xys = np.zeros(shape=(height, width, 2), dtype=float)

    cdef int i, j

    for i in range(height):  # , nogil=True, num_threads=c_count_square):
        for j in range(width):  # , num_threads=c_count_square):
            xys[i, j, 0] = i
            xys[i, j, 1] = j

    return np.asarray(xys, dtype=float)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef apply_roi(double[:, :] depths, double[:, :, :] roi_coords):

    cdef int h = roi_coords.shape[0], w = roi_coords.shape[1]
    cdef int i, j, ii, ij, length = h * w
    cdef double x, y

    cdef double[:, :] points = np.zeros(shape=(length, 3), dtype=float)

    for i in prange(h, nogil=True, num_threads=c_count_square):
        ii = i * w
        for j in prange(w, num_threads=c_count_square):
            ij = ii + j
            x = roi_coords[i, j, 0]
            y = roi_coords[i, j, 1]
            points[ij, 0] = x
            points[ij, 1] = y
            points[ij, 2] = depths[int(x), int(y)]

    return np.asarray(points)


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef apply_depth_scale(double[:, :] coordinates, double scale):

    cdef double[:, :] temp_depths
    cdef int i, j
    cdef int r = coordinates.shape[0]

    if coordinates.shape[0] > 0:
        # print(coordinates.shape)
        temp_depths = np.zeros(shape=(coordinates.shape[0], coordinates.shape[1]), dtype=float)

        for i in prange(r, nogil=True, num_threads=c_count):
            for j in range(2):
                temp_depths[i, j] = coordinates[i, j]
            temp_depths[i, 2] = coordinates[i, 2] * scale

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

        colors[i, 0] = r if 0 <= r <= 1 else 0 if r < 0 else 1
        colors[i, 1] = g if 0 <= g <= 1 else 0 if g < 0 else 1
        colors[i, 2] = b if 0 <= b <= 1 else 0 if b < 0 else 1
        colors[i, 3] = 1

    return np.asarray(colors)


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef split_data(double[:, :] frame, int h, int w, int num):

    cdef int row_col_len = int(sqrt(num))
    # print("frame shape is: {}, w is {}, and h is {}".format(frame.shape, w, h))
    cdef int w_inc = w // row_col_len
    cdef int h_inc = h // row_col_len

    cdef double[:, :, :] bits = np.zeros(shape=(num, w_inc, h_inc), dtype=float)
    cdef int i, j, k, ij, ik
    cdef double temp

    for i in prange(num, nogil=True, num_threads=c_count_square):
        ij = i // row_col_len
        ik = i - row_col_len * ij
        for j in prange(w_inc, num_threads=c_count_square):
            for k in prange(h_inc):
                # print("Calculating index with parts {} {} {} for a result of {}".format(ij, w_inc, j, ij * w_inc + j))
                temp = frame[ik * h_inc + k, ij * w_inc + j]
                bits[i, j, k] = temp

    return bits


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef concatenate_bits(double[:, :, :] points, long[:] counts):

    cdef int sum = 0, i, j

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

    return conc


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef convert_to_points(double[:, :, :] bits, int h, int w, int interpolation):

    cdef int max_num = w * h
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


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef scatter_data(double[:, :] depths, object validator=None,
                         int h=-1, int w=-1, int interpolation=1):

    # Handles if h or w is -1 (default)
    if h < 0 or w < 0:
        h = depths.shape[0] if h < 0 else h
        w = depths.shape[1] if w < 0 else w
        # print("h is {} and w is {}".format(h, w))

    cdef double[:, :, :] bits = split_data(depths, h, w, c_count)
    # print("bits shape is {}".format(bits.shape))

    cdef double[:, :, :] points
    cdef long[:] counts

    points, counts = convert_to_points(bits, h, w, interpolation)

    cdef double[:, :] concatenated = concatenate_bits(points, counts)

    return np.asarray(concatenated)  # , x_cen, y_cen, z_cen
