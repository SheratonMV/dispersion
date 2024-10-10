import numpy as np


def matcher(distances, indices, color, retarr, retdistarr):
    for i in range(0, len(indices)):
        a = color[indices[i]]
        val = np.where(a != a[0])[0]
        if len(val)!=0:
            retarr[i] = val[0]
            retdistarr[i]= distances[i][val[0]]
    return retarr, retdistarr