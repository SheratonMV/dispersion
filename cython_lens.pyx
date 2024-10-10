# cython: language_level=2, boundscheck=False
import numpy as np
cimport numpy as np

def lens(np.uint16_t [:] x, int center, int breaker):
    # y = np.reshape(x, (2, filtersize, filtersize))
    # p = np.sum(y[0:-1]) * y[-1, 1, 1]
    cdef int inb = x[-center]
    if inb == 0:
        return 0
    x[breaker:] = 0
    # q = np.sum(x) * inb
    # if q>0:
    #     a=1
    return np.sum(x) * inb

