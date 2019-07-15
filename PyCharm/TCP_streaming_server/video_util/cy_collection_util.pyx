import cython
from cpython cimport array
import array
import io
from PIL import Image
cimport numpy as np
import numpy as np


# region bytes conversion

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


cpdef rgb_to_bytes(unsigned char[:, :, :] frame, const unsigned char[:] buff):
    cdef int orig, comp
    cdef double ratio
    cdef unsigned char[:] b

    orig = np.asarray(frame).size
    img = Image.fromarray(np.asarray(frame))
    img.save(buff, 'JPEG', quality=30, optimize=True)

    b = buff.getvalue()

    comp = len(b)
    ratio = comp / orig

    if ratio > 1:
        ratio = 1.0
        b = bytes(np.asarray(frame).reshape(-1))

    return bytes(b, 'latin-1'), ratio


cpdef bytes_to_depth(bytes depth_bytes, int dtype, int height, int width):
    cdef unsigned short[:] darr
    # cdef double[:] dtarr
    cdef unsigned short[:, :] drearr
    cdef unsigned char[:] arr
    cdef unsigned char[:, :] grearr
    cdef unsigned char[:, :, :] rearr

    if dtype == 2:
        darr = np.asarray(array.array('H', depth_bytes))
        # dtarr = np.multiply(darr, 1 / 65536)
        drearr = np.reshape(darr, (height, width))
        return np.rot90(np.asarray(drearr))
    elif dtype == 1:
        arr = np.asarray(array.array('B', depth_bytes))
        grearr = np.reshape(arr, (height, width))
        return np.rot90(np.asarray(grearr))
    else:
        arr = np.asarray(array.array('B', depth_bytes))
        rearr = np.reshape(arr, (height, width, -1))
        return np.rot90(np.asarray(rearr))

# endregion


@cython.boundscheck(False)
cpdef convert_realsense(object frames, double scale, int rgb, int ir, int depth):
    cdef unsigned char[:, :, :] rgb_frame = np.zeros(shape=(1, 1, 1), dtype=np.uint8)
    cdef unsigned char[:, :] ir_frame = np.zeros(shape=(1, 1), dtype=np.uint8)
    cdef unsigned short[:, :] depth_image = np.zeros(shape=(1, 1), dtype=np.uint16)

    if rgb > 0:
        rgb_frame = np.asanyarray(frames.get_color_frame().get_data(),
                                  dtype=np.uint8)[..., ::-1]  # Converts BGR -> RGB using numpy

    if ir > 0:
        ir_frame = np.asanyarray(frames.get_infrared_frame().get_data(), dtype=np.uint8)

    if depth > 0:
        depth_image = np.asanyarray(frames.get_depth_frame().get_data(), dtype=np.uint16)

    # depth_image = depth_image / depth_image.max()
    
    return np.asarray(rgb_frame), np.asarray(ir_frame), np.asarray(depth_image)


@cython.cdivision(True)
@cython.boundscheck(False)
cpdef average_depth(unsigned short[:, :] coordinates):
    cdef double sum = 0, current = 0, mn = 65536, mx = 0
    cdef int count = 0, i, j
    cdef int height = coordinates.shape[0], width = coordinates.shape[1], length = height * width

    cdef double[:] depths = np.zeros(shape=length, dtype=float)

    for i in range(height):  # , nogil=True, num_threads=c_count):
        for j in range(width):
            current = coordinates[i, j]

            if current > 0:
                if current < mn:
                    mn = current
                if current > mx:
                    mx = current

                sum += current
                count += 1

    if count > 0:
        return sum / float(count), mn, mx
    else:
        return 0, 0, 0
    