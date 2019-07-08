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


cdef perform_vector_walk(double[:, :] frame, int x, int y, int origin_x, int origin_y):
    cdef char up = 0, left = 0

    if origin_x <= x:
        left = 1

    if origin_y <= y:
        up = 1

    cdef int delta_x = x - origin_x - 1, delta_y = y - origin_y - 1
    cdef char vertical = 1 if delta_x < delta_y else 0
    cdef int segment = int(delta_y / delta_x) if vertical == 1 else int(delta_x / delta_y)
    cdef int i, j

    if left == 1:
        if up == 1:
            if vertical == 1:
                for i in range(x - 1, origin_x, -1):






cdef double roughness_factor(double[:, :] frame, double average):
    """Calculates the roughness factor, which is found by applying the following formula:
    
    number of distinct peaks * average peak-to-peak magnitude
    --------------------------------------------------------- = Roughness
                   average peak duty-cycle
                   
    """

    # region variable definitions

    cdef double roughness, num_peaks, magnitude

    cdef int i, j, first = 1, height = frame.shape[0], width = frame.shape[1]
    cdef int area = height * width
    cdef double value

    # Peak detection variables

    cdef int[:, :] peaks = np.zeros(shape=(height, width), dtype=int), dc_markers = np.zeros(shape=(height, width), dtype=int)
    cdef int peak_found = 0

    # For calculating the troughs
    cdef double[:] embedded_magnitudes = np.zeros(shape=area, dtype=float)
    cdef int em_mag_index = 0

    cdef double[:] radii
    cdef double radius
    cdef int mi, mj, current_radii, angle

    # Magnitude placeholders
    cdef double[:] magnitudes = np.zeros(shape=area, dtype=float)
    cdef int magnitude_index = 0

    # Duty-Cycle placeholders
    cdef double time_off = 0, time_on = 0
    cdef double[:] dc = np.zeros(shape=area, dtype=float)
    cdef int dc_index = 0

    # Peak count placeholders
    cdef double peak_count = 0

    # endregion

    # TODO peak_count will always be half of the magnitude index

    """ Start moving downwards through the image, searching for peaks,
    You know you've found a peak when:
        You were already rising
        Every previous value if less
    """
    for i in range(height):         # row
        for j in range(width):      # column
            value = frame[i, j]

            # Duty cycle check
            if value > average:
                dc_markers[i, j] = 1

            # region Peak detection

            peak_found = 0

            # (-1, -1), (-1, 0), (-1, 1)
            # (0, -1),    N/A,   (0, 1)
            # (1, -1),  (1, 0),  (1, 1)
            if i > 0:
                # (-1, 0)
                if value > frame[i -1, j]:
                    if j > 0:
                        # (-1, -1), (0, -1)
                        if value > frame[i - 1, j - 1] and value > frame[i, j - 1]:
                            if i < height - 1:
                                # (1, 0), (1, -1)
                                if value > frame[i + 1, j] and value > frame[i + 1, j - 1]:
                                    if j < width - 1:
                                        # (0, 1), (-1, 1), (1, 1)
                                        if value > frame[i, j + 1] and value > frame[i - 1, j + 1] and value > frame[i + 1, j + 1]:

                                            peak_found = 1
                                    else:
                                        peak_found = 1

                            elif j < width - 1:
                                # (0, 1), (-1, 1)
                                if value > frame[i, j + 1] and value > frame[i - 1, j + 1]:
                                    peak_found = 1
                    elif i < height - 1:
                        # (1, 0)
                        if value > frame[i + 1, j]:
                            if j < width - 1:
                                # (0, 1), (-1, 1), (1, 1)
                                if value > frame[i, j + 1] and value > frame[i - 1, j + 1] and value > frame[i + 1, j + 1]:

                                    peak_found = 1
                            else:
                                peak_found = 1

                    elif j < width - 1:
                        # (0, 1), (-1, 1)
                        if value > frame[i, j + 1] and value > frame[i - 1, j + 1]:
                            peak_found = 1
            elif j > 0:
                # (0, -1)
                if value > frame[i, j - 1]:
                    if i < height - 1:
                        # (1, 0), (1, -1)
                        if value > frame[i + 1, j] and value > frame[i + 1, j - 1]:
                            if j < width - 1:
                                # (0, 1), (1, 1)
                                if value > frame[i, j + 1] and value > frame[i + 1, j + 1]:

                                    peak_found = 1
                            else:
                                peak_found = 1

                    elif j < width - 1:
                        # (0, 1)
                        if value > frame[i, j + 1]:
                            peak_found = 1
            elif i < height - 1:
                # (1, 0)
                if value > frame[i + 1, j]:
                    if j < width - 1:
                        # (0, 1), (1, 1)
                        if value > frame[i, j + 1] and value > frame[i + 1, j + 1]:

                            peak_found = 1
                    else:
                        peak_found = 1

            elif j < width - 1:
                # (0, 1)
                if value > frame[i, j + 1]:
                    peak_found = 1

            if peak_found == 1 and dc[i, j] == 1:
                peaks[i, j] = 1

            # endregion

            # TODO For each peak, look for lower peaks in a 360 degree circle around it, average these
            # TODO If you hit another peak during this rotation and it's taller than you, then set this peak value to 0 and break

            radii = np.zeros(shape=4, dtype=float)
            current_radii = 0

            if i > 0:
                # i is not 0

                # (0, w)
                mi = height - i - 1
                mj = width - j - 1
                radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                current_radii += 1

                # (0, 0)
                radii[current_radii] = sqrt(float(i * i + j * j))
                current_radii += 1

                if j > 0:
                    # j is not 0

                    # (h, 0)
                    mi = height - i - 1
                    radii[current_radii] = sqrt(float(mi * mi + j * j))
                    current_radii += 1

                    if i < height - 1:
                        if j < width - 1:

                            # (h, w)
                            mi = height - i - 1
                            mj = width - j - 1
                            radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                            current_radii += 1

                elif i < height - 1:
                    # j is 0

                    # (h, 0)
                    mi = height - i - 1
                    radii[current_radii] = sqrt(float(mi * mi + j * j))
                    current_radii += 1

                    # (h, w)
                    mi = height - i - 1
                    mj = width - j - 1
                    radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                    current_radii += 1

                else:
                    # i is h, j is 0

                    # (h, w)
                    mi = height - i - 1
                    mj = width - j - 1
                    radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                    current_radii += 1

            elif j > 0:
                # i is 0

                # (h, 0)
                mi = height - i - 1
                radii[current_radii] = sqrt(float(mi * mi + j * j))
                current_radii += 1

                # (0, 0)
                radii[current_radii] = sqrt(float(i * i + j * j))
                current_radii += 1

                # (h, w)
                mi = height - i - 1
                mj = width - j - 1
                radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                current_radii += 1

                if j < width - 1:

                    # (0, w)
                    mi = height - i - 1
                    mj = width - j - 1
                    radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                    current_radii += 1

            else:

                # (h, 0)
                mi = height - i - 1
                radii[current_radii] = sqrt(float(mi * mi + j * j))
                current_radii += 1

                # (h, w)
                mi = height - i - 1
                mj = width - j - 1
                radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                current_radii += 1

                # (0, w)
                mi = height - i - 1
                mj = width - j - 1
                radii[current_radii] = sqrt(float(mi * mi + mj * mj))
                current_radii += 1

            radius = max(radii)

            for mi in range(height):
                if mi == 0 or mi == height - 1:
                    for mj in range(width):
                        perform_vector_walk(frame, i, j, mi, mj)
                else:
                    mj = 0
                    perform_vector_walk(frame, i, j, mi, mj)
                    mj = width - 1
                    perform_vector_walk(frame, i, j, mi, mj)



@cython.boundscheck(False)
cpdef convert_realsense(object frames, double[:, :] roi, int u, int b, int l, int r):

    cdef double[:, :] depth_image = np.multiply(np.asanyarray(frames.get_depth_frame().get_data()), 1).astype(float)  # scale)
    # depth_image = depth_image / depth_image.max()

    cdef int i, j
    cdef double rms_sum, count, temp, frame_avg, val_temp
    cdef int width, height

    width = depth_image.shape[0]
    height = depth_image.shape[1]

    cdef int std_index = 0
    cdef double[:] std_dev = np.zeros(shape=width * height, dtype=float)

    # print(np.asarray(history))
    rms_sum = 0
    count = 0

    for i in range(u, b, 1):  # , nogil=True):
        for j in range(l, r, 1):
            val_temp = depth_image[i, j]

            if depth_image[i, j] > 0:
                rms_sum += val_temp * val_temp
                count += 1

                std_dev[std_index] = depth_image[i, j]
                std_index += 1

                temp = depth_image[i, j]  # // depth_clumping) % 2) * 255
                # print("Result {}".format(temp))
                roi[i - u, j - l] = temp

    cdef double[:] adj_pop = std_dev[:std_index]

    if count > 0:
        frame_avg = sqrt(rms_sum / count)
    # cdef double[:, :] norm = normal_distribution(adj_pop, frame_avg)

    return np.asarray(roi), np.asarray(adj_pop), frame_avg  # std_dev[:std_index])
