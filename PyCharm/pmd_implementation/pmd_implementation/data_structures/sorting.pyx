import cython
from cython.parallel import prange
from cpython cimport array
import array
cimport numpy as np
import numpy as np
import os


# @cython.cdivision(True)
# @cython.boundscheck(False)
cdef void heapify(double[:] arr, int length, int index):

    cdef int largest = index
    cdef int left = 2 * index + 1
    cdef int right = 2 * index + 2

    # print("Heapifying {} {} {}".format(arr[index], arr[left] if left < length else 'None', arr[right] if right < length else 'None'))

    if left < length and arr[index] < arr[left]:
        # print("{} is larger than {}".format(arr[left], arr[index]))
        largest = left

    if right < length and arr[largest] < arr[right]:
        # print("{} is larger than {}".format(arr[right], arr[largest]))
        largest = right

    if largest != index:
        arr[index], arr[largest] = arr[largest], arr[index]
        heapify(arr, length, largest)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef heapsort(double[:] arr):
    cdef int n = arr.shape[0]

    cdef int i, ii
    cdef int[:] rev = array.array('i', range((n >> 1) - 1, -1, -1))

    for i in range(len(rev)):
        ii = rev[i]
        heapify(arr, n, ii)
        # print("Array after heapifying index {}: {}".format(ii, np.asarray(arr)))

    # print(np.asarray(arr))

    rev = array.array('i', range(n - 1, 0, -1))

    for i in range(len(rev)):
        ii = rev[i]
        arr[ii], arr[0] = arr[0], arr[ii]
        heapify(arr, ii, 0)


# @cython.cdivision(True)
# @cython.boundscheck(False)
cpdef binary_search(double[:] arr, double value, bint ascending, bint round_up):
    """Performs a binary search for a value in the array, returns the closest element it found,
    rounding up if specified, but defaults to rounding down."""

    cdef length, mid, start = 0, stop = arr.shape[0]
    cdef double, current

    length = stop - start
    mid = start + (length >> 1)

    if mid < arr.shape[0]:
        current = arr[mid]

    while length > 2 and mid != stop and current != value:
        current = arr[mid]
        if value > current:
            if ascending:
                start = mid
            else:
                stop = mid
        else:
            if ascending:
                stop = mid
            else:
                start = mid

        length = stop - start
        mid = start + (length >> 1)

    if current == value:
        return mid
    else:
        if value > current:
            if round_up:
                return mid + 1 if mid < arr.shape[0] else mid
            else:
                return mid
        else:
            if round_up:
                return mid
            else:
                return mid - 1 if mid > 0 else mid
