import numpy as np
from fipy import dump
import sys
import cv2
import time
from ctypes import CDLL, c_double, POINTER, c_int
from skimage.color import deltaE_ciede2000
from numpy.ctypeslib import ndpointer

global resclone

def ce2000(allcolors, manualcolors, size, manualsize):  # c++ based function
    global resclone
    adder = CDLL('cppcompilation/color_reducer.dll')
    adder.simplecolors.argtypes = [POINTER(c_double), POINTER(c_double), POINTER(c_double), POINTER(c_double),
                                   POINTER(c_double), POINTER(c_double),
                                   POINTER(c_int), c_int, c_int]
    adder.simplecolors.restype = ndpointer(dtype=c_int, shape=(size,))  # POINTER(c_int)

    input_arrayl = np.array(allcolors[:, 0], dtype=np.float64)
    input_arraya = np.array(allcolors[:, 1], dtype=np.float64)
    input_arrayb = np.array(allcolors[:, 2], dtype=np.float64)
    input_arrayl2 = np.array(manualcolors[:, 0], dtype=np.float64)
    input_arraya2 = np.array(manualcolors[:, 1], dtype=np.float64)
    input_arrayb2 = np.array(manualcolors[:, 2], dtype=np.float64)
    input_ptrl = input_arrayl.ctypes.data_as(POINTER(c_double))
    input_ptra = input_arraya.ctypes.data_as(POINTER(c_double))
    input_ptrb = input_arrayb.ctypes.data_as(POINTER(c_double))
    input_ptrl2 = input_arrayl2.ctypes.data_as(POINTER(c_double))
    input_ptra2 = input_arraya2.ctypes.data_as(POINTER(c_double))
    input_ptrb2 = input_arrayb2.ctypes.data_as(POINTER(c_double))
    output_intarr = np.ones_like(input_arrayl, dtype=int) * size

    output_intarrc = output_intarr.ctypes.data_as(POINTER(c_int))
    # for ii in range(size):
    # print (size, manualsize)
    res_int = adder.simplecolors(input_ptrl, input_ptra, input_ptrb, input_ptrl2, input_ptra2, input_ptrb2,
                                 output_intarrc,
                                 size, manualsize)
    # print("out", np.unique(res_int))
    del input_ptrl, input_ptra, input_ptrb, input_ptrl2, input_ptra2, input_ptrb2, output_intarrc
    resclone = np.copy(res_int)
    # print(np.unique(resclone))
    # closeness = np.ctypeslib.as_array(res_int, shape=input_arrayl.shape)
    return res_int


def ciedesklearn(allcolors, size):
    save_arr = np.zeros((size, size))
    allcolors = allcolors.astype(np.float32)
    for colcount in range(size):
        templab = deltaE_ciede2000(allcolors, allcolors[colcount], kL=1.0, kC=1.0, kH=0.1)
        save_arr[colcount] = np.copy(templab)
    return np.argmin(save_arr, axis=0)


def specscleaner(imgscan):
    grayImage = cv2.cvtColor(imgscan, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 0, 255, cv2.THRESH_BINARY)
    spots_bef = np.where(blackAndWhiteImage != 0)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(blackAndWhiteImage, connectivity=8)
    # connectedComponentswithStats yields every seperated component with information on each of them, such as size
    # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
    sizes = stats[1:, -1];
    nb_components = nb_components - 1

    # minimum size of particles we want to keep (number of pixels)
    # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
    min_size = 15

    # your answer image
    img2 = np.zeros((output.shape))
    # for every component in the image, you keep it only if it's above min_size
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255

    spots_aft = np.where(img2 != 0)
    return np.where(img2 == 0)


def color_reduction(filename, parentdirectory, avgcellsize=1):
    global resclone
    kleurcutoff = 80
    kL = 1.0
    kC = 1.0
    kH = 0.1
    colos = cv2.cvtColor(cv2.imread("outputs/" + parentdirectory + "/" + filename), cv2.COLOR_BGR2Lab)
    actualshape = colos.shape
    colos = colos.reshape(-1, 3)
    manualcolors = np.loadtxt("outputs/" + parentdirectory + "/colors.dat", unpack=True,
                              delimiter=',').transpose().astype(np.uint8)
    manualcolors = cv2.cvtColor(np.asarray([manualcolors]), cv2.COLOR_BGR2Lab)
    manualcolors = manualcolors.reshape(-1, 3)
    # colos = dump.read("outputs/" + parentdirectory + "/temp/" + filename + ".dat")
    maxsinglerun = 10000
    resultarr = np.zeros(len(colos), dtype=int)
    start = time.time()
    count = 1
    for i in range(0, len(colos), maxsinglerun):
        if i != 0:
            msg = "Step 1 : item %i of %i" % (count, int(len(colos) / maxsinglerun))
            sys.stdout.write(msg + chr(8) * len(msg))
            sys.stdout.flush()
            count += 1
            sweep = i
            bottom = sweep - maxsinglerun
            coloslab = colos[bottom:sweep]
            m = ce2000(coloslab, manualcolors, len(coloslab), len(manualcolors))
            # print(bottom, sweep, np.unique(m), np.unique(resclone))
            resultarr[bottom:sweep] = np.copy(resclone)

            # print (np.unique(resultarr))
    sweep = len(colos)
    bottom = i
    coloslab = colos[bottom:sweep]
    m = ce2000(coloslab, manualcolors, len(coloslab), len(manualcolors))

    resultarr[bottom:sweep] = np.copy(resclone)
    del m
    # finalimage = cv2.cvtColor(manualcolors[resultarr].reshape(actualshape), cv2.COLOR_Lab2BGR)
    # cv2.imwrite("outputs/" + parentdirectory + "/1" + filename, finalimage)
    del colos
    resultarr = resultarr.reshape((actualshape[0], actualshape[1]))
    chncount = 0
    manualcolors = cv2.cvtColor(np.asarray([manualcolors]), cv2.COLOR_Lab2BGR)
    manualcolors = manualcolors.reshape(-1, 3)
    uniquefound = np.unique(resultarr)
    print("Colors found =", len(uniquefound) - 1)
    finalimg = np.zeros(actualshape, dtype=np.uint8)
    cellcounts = list()
    for j in uniquefound:
        if j != 0:
            tempimg = np.zeros(actualshape, dtype=np.uint8)
            # tempbw = np.zeros((actualshape[0], actualshape[1]), dtype=np.uint8)
            # kernel = np.ones((3, 3), np.uint8)
            chnind = np.where(resultarr == j)
            # tempbw[chnind] = 255
            # tempbw = cv2.erode(tempbw, kernel, iterations=1)
            # tempbw = cv2.dilate(tempbw, kernel, iterations=1)
            # chnind = np.where(tempbw == 255)
            tempimg[chnind] = manualcolors[j]
            # cv2.imwrite(
            #     "outputs/" + parentdirectory + "/temp/free" + str(kleurcutoff) + str(kL) + str(kC) + str(
            #         kH) + "_" + str(
            #         chncount) + "_" + filename, tempimg)
            # specfreeind = specscleaner(tempimg)
            print("Channel", j, "nos:", len(chnind[0]), "Possible cell count:", len(chnind[0])/avgcellsize)
            cellcounts.append(len(chnind[0]))
            # tempimg[specfreeind] = (0, 0, 0)
            finalimg += tempimg
            cv2.imwrite(
                "outputs/" + parentdirectory + "/temp/" + str(kleurcutoff) + str(kL) + str(kC) + str(kH) + "_" + str(
                    chncount) + "_" + filename, tempimg)
            chncount += 1
    # finalimg = cv2.cvtColor(finalimg, cv2.COLOR_Lab2BGR)
    cv2.imwrite("outputs/" + parentdirectory + "/1" + filename, finalimg)
    # n = ciedesklearn(coloslab, len(coloslab))
    k = (time.time() - start) / 60.

    # print("Time taken for color reduction:", k)
    a = 1
    np.savetxt("outputs/" + parentdirectory + "/temp/" + "colorcounts.txt", cellcounts)
    return cellcounts
#
# parentdirectory = "ibidi"  # "Tile7"
# filename = "TileScan1A1Merged.tif"
# color_reduction(filename, parentdirectory)
