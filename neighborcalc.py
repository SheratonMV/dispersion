import cv2
import numpy as np
import os
from scipy import ndimage
import time
# from cython_lens import lens
from gfilter import sumfilter, heterofilter
import nearest_dist_neighbor
def lens(x, center, breaker):
    # y = np.reshape(x, (2, filtersize, filtersize))
    # p = np.sum(y[0:-1]) * y[-1, 1, 1]
    inb = x[-center]
    if inb == 0:
        return 0
    x[breaker:] = 0
    # q = np.sum(x) * inb
    # if q>0:
    #     a=1
    return np.sum(x) * inb


def chn_totals(parentdirectory):
    outputdir = 'outputs/' + parentdirectory + '/temp'
    files = os.listdir(outputdir)
    allsplits = list()
    channelnumber = list()
    channelpaths = list()
    for names in files:
        if 'min_dist' not in names:
            namesplit = names.split('_')
            if len(namesplit) == 3:
                allsplits.append(names)
                channelnumber.append(int(namesplit[1]))
                channelpaths.append('')
    count = -1
    for i in channelnumber:
        count += 1
        channelpaths[i] = allsplits[count]
    return len(channelpaths)


def image_gen(parentdirectory):
    start = time.time()
    outputdir = 'outputs/' + parentdirectory + '/temp'
    files = os.listdir(outputdir)
    allsplits = list()
    channelnumber = list()
    channelpaths = list()
    for names in files:
        if 'min_dist' not in names:
            namesplit = names.split('_')
            if len(namesplit) == 3:
                allsplits.append(names)
                channelnumber.append(int(namesplit[1]))
                channelpaths.append('')
    count = -1
    for i in channelnumber:
        count += 1
        channelpaths[i] = allsplits[count]
    sample = cv2.imread(outputdir + "/" + channelpaths[0], 0)
    original_images = np.zeros((len(channelpaths), sample.shape[0], sample.shape[1]), dtype=np.uint8)
    sum_images = np.zeros((len(channelpaths), sample.shape[0], sample.shape[1]), dtype=np.uint8)
    count = 0
    for path in channelpaths:
        original_images[count] = cv2.imread(outputdir + "/" + path, 0)
        count += 1
    original_images[original_images > 0] = 1
    for i in range(0, len(channelpaths)):
        locpos = np.ones((len(channelpaths), 1, 1), dtype=bool)
        locpos[i] = False
        sum_images[i] = np.sum(original_images * locpos, axis=0)

    for i in range(0, len(channelpaths)):
        output = nearest_dist_neighbor.run(np.where(original_images[i] == 1), np.where(sum_images[i] == 1))

        cv2.imwrite(outputdir + "/" + "sum_" + str(i) + ".tif", sum_images[i])
        np.savetxt(outputdir + "/" + "min_dist_" + str(i) + ".txt", output)
        cv2.imwrite(outputdir + "/" + "org_" + str(i) + ".tif", original_images[i])
    end = time.time()
    # print((end - start) / 60.)


def neighbors(parentdirectory, chn, filtersize):
    start = time.time()
    outputdir = 'outputs/' + parentdirectory + '/temp'
    # filtersize = 3
    # filtersize2 = 11111
    fp = np.ones((2, filtersize, filtersize), dtype=int)
    fp2 = np.ones((filtersize, filtersize), dtype=int)

    imorg = (cv2.imread(outputdir + "/" + "org_" + str(chn) + ".tif", 0))  # .astype(int)
    imsum = cv2.imread(outputdir + "/" + "sum_" + str(chn) + ".tif", 0)
    im = np.zeros((2, imorg.shape[0], imorg.shape[1]))
    im[0] = imsum
    im[1] = imorg
    del imsum
    midpoint = int((filtersize - 1) / 2)
    fp2[midpoint, midpoint] = 0
    # im[0] = 1
    center = int(((filtersize * filtersize) + 1) / 2)
    breaker = int(filtersize * filtersize)
    # butcenter = breaker + (filtersize * filtersize) / 2
    sumfilter = ndimage.generic_filter(im.astype(np.uint16), function=lens, mode='constant', cval=0, footprint=fp,
                                       extra_arguments=(center, breaker))
    homofilter = ndimage.generic_filter(imorg.astype(np.uint16), function=np.sum, mode='constant', cval=0,
                                        footprint=fp2)
    finish = time.time()
    print((finish - start) / 3600.)
    homofilter = (homofilter + 1)
    homofilter = homofilter.astype(np.float)
    mixratio = sumfilter[1] / homofilter
    spots = sumfilter != 0
    spots2 = imorg != 0
    print(np.sum(sumfilter[1]), np.max(sumfilter[1]), np.median(sumfilter[spots]), sumfilter[spots].mean(), mixratio[spots2].mean())
    return [chn, filtersize, np.sum(sumfilter[1]), np.max(sumfilter[1]), np.median(sumfilter[spots]),
            sumfilter[spots].mean(), mixratio[spots2].mean()]


def neighbors2(parentdirectory, chn, filtersize):
    start = time.time()
    outputdir = 'outputs/' + parentdirectory + '/temp'
    imorg = cv2.imread(outputdir + "/" + "org_" + str(chn) + ".tif", 0)
    imsum = cv2.imread(outputdir + "/" + "sum_" + str(chn) + ".tif", 0)
    hetero = np.zeros_like(imorg, dtype=np.uint16)
    heterofilter(imorg, imsum, hetero, imorg.shape[0], imorg.shape[1], filtersize)
    homo = np.zeros_like(imorg, dtype=np.uint16)
    sumfilter(imorg, homo, imorg.shape[0], imorg.shape[1], filtersize)
    homo = homo+1
    homo = homo.astype(float)
    mixratio = hetero / (homo+hetero)
    spots = hetero != 0
    spots2 = imorg != 0
    finish = time.time()
    # print(np.sum(hetero), np.max(hetero), np.median(hetero[spots]), hetero[spots].mean(), mixratio[spots2].mean())
    # print((finish - start) / 60.)
    return [chn, filtersize, np.sum(hetero), np.max(hetero), np.median(hetero[spots]),
            hetero[spots].mean(), mixratio[spots2].mean()]


# neighbors("invivo/ls180", 2, 3)
# neighbors2("invivo/ls180", 2, 101)
