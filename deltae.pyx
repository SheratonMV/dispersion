# cython: language_level=2, boundscheck=False
from ctypes import CDLL, c_double, POINTER, c_int
import numpy as np
cimport numpy as np
import multiprocessing
# load the shared object file

from cython.parallel import prange
import time
# Find sum of integers

cdef c2000(np.uint8_t [:,:] allcolors, np.float_t [:] closeness, int size, adder):
    cdef Py_ssize_t ii
    cdef Py_ssize_t jj
    cdef np.float_t res_int
    input_arrayl = np.array(allcolors[:][0], dtype=np.float64)
    input_arraya = np.array(allcolors[:][1], dtype=np.float64)
    input_arrayb = np.array(allcolors[:][2], dtype=np.float64)

    input_ptrl = input_arrayl.ctypes.data_as(POINTER(c_double))
    input_ptra = input_arraya.ctypes.data_as(POINTER(c_double))
    input_ptrb = input_arrayb.ctypes.data_as(POINTER(c_double))
    #for ii in range(size):
    res_int = adder.CIEDE2000(input_ptrl, input_ptra, input_ptrb, input_ptrl, input_ptra, input_ptrb, size)
        # for jj in range(size):
        #     res_int = adder.CIEDE2000(input_ptrl,input_ptra,input_ptrb,input_ptrl,input_ptra,input_ptrb, size)
        #     if res_int<closeness[ii]:
        #         if res_int!=0:
        #             closeness[ii] = res_int
    return closeness

def ce2000(np.uint8_t [:,:] allcolors, np.float_t [:] closeness, int size):
    cdef adder = CDLL('./CIEDE2000/adder.so')
    adder.CIEDE2000.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double), c_int]
    adder.CIEDE2000.restype = c_double
    print (type(adder))
    c2000(allcolors, closeness, size, adder)
    return closeness