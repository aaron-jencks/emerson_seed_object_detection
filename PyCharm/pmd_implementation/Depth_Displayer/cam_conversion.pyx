import cython
from cython.parallel import prange

cimport numpy as np
import numpy as np


cdef extern from "math.h":
    double sqrt(double x)


cdef int ceiling(double val):
    if val > int(val):
        return int(val) + 1
    else:
        return int(val)


cdef int get_clump_i_coord(int i, int clumping):
    return i // clumping


cdef int get_clump_j_coord(int j, int clumping):
    return j // clumping


cdef double average(double[:, :, :] history, int i, int j) except -1:
    # print("{} {}".format(i, j))
    cdef double[:] s = history[:, i, j]

    return sum(s) / float(s.shape[0])


@cython.boundscheck(False)
cdef double[:, :] normal_distribution(double[:] pop):
    """Calculates the standard deviation for this population"""

    cdef int p
    cdef double std_dev, dev_sum = 0, dev_temp
    cdef double avg = sum(pop) / float(pop.shape[0])

    # Calculates the standard deviation
    for p in prange(pop.shape[0], nogil=True):
        dev_temp = pop[p] - avg
        dev_sum += dev_temp * dev_temp

    std_dev = sqrt(dev_sum / float(pop.shape[0]))

    # Calculates the z-values
    cdef double[:, :] result = np.zeros(shape=(pop.shape[0], 2), dtype=float)

    for p in prange(pop.shape[0], nogil=True):
        result[p, 0] = pop[p]
        if std_dev != 0:
            result[p, 1] = ((pop[p] - avg) / std_dev)
        else:
            result[p, 1] = 0

    return result


@cython.boundscheck(False)
cpdef convert_realsense(object frames, float[:, :] roi, int u, int b, int l, int r,
                        int clumping, int depth_clumping,
                        int create_history, double[:, :, :] history, int history_depth):

    cdef double[:, :] depth_image = np.multiply(np.asanyarray(frames.get_depth_frame().get_data()), 1).astype(float)  # scale)
    # depth_image = depth_image / depth_image.max()

    cdef int i, j, clump_index_i, clump_index_j, c_i, c_j, ret, i_temp
    cdef double rms_sum, count, history_sum, history_count, temp
    cdef int width, height

    width = ceiling(depth_image.shape[0]  / clumping)
    height = ceiling(depth_image.shape[1] / clumping)

    cdef double[:, :] clump_array = np.zeros(shape=(width, height), dtype=float)

    cdef int std_index = 0
    cdef double[:] std_dev = np.zeros(shape=width * height, dtype=float)

    # Creates history array
    if create_history == 1:
        history = np.zeros(shape=(history_depth, depth_image.shape[0], depth_image.shape[1]), dtype=float)

    # Updates the history array
    for i in prange(u, b, 1, nogil=True):
        for j in prange(l, r, 1):

            # Calculates historical average
            i_temp = 0
            for i_temp in range(1, history.shape[0]):
                # print(temp)
                history[i_temp - 1, i, j] = history[i_temp, i, j]

            history[history.shape[0] - 1, i, j] = depth_image[i, j]


    # print(np.asarray(history))

    for i in range(u, b, 1):  # , nogil=True):
        for j in range(l, r, 1):

            # Calculates the clumping
            clump_index_i = (i - u) // clumping
            clump_index_j = (j - l) // clumping

            if clump_array[clump_index_i, clump_index_j] == 0:
                rms_sum = 0
                count = 0

                for c_i in prange(i, i + clumping, 1, nogil=True):
                    for c_j in prange(j, j + clumping, 1):
                        # temp = average(history, c_i, c_j)

                        history_count = 0
                        history_sum = 0
                        for i_temp in range(1, history.shape[0]):
                            history_sum = history_sum + history[i_temp, i, j]
                            history_count = history_count + 1

                        temp = history_sum / history_count

                        rms_sum += temp * temp
                        count += 1

                # print("Actual clump: {}".format(sqrt(rms_sum / count)))
                clump_array[clump_index_i, clump_index_j] = sqrt(rms_sum / count)

            std_dev[std_index] = clump_array[clump_index_i, clump_index_j]
            std_index += 1

            temp = float(int(clump_array[clump_index_i, clump_index_j] // depth_clumping) % 2) * 255
            # print("Result {}".format(temp))
            roi[i - u, j - l] = temp

    cdef double[:, :] norm = normal_distribution(std_dev[:std_index])

    return np.asarray(history, dtype=float), np.asarray(roi), np.asarray(std_dev[:std_index])
