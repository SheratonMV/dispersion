import cv2
import numpy as np
import sys
import os
import time
import subprocess

import parallel_neigh
from neighborcalc import image_gen
from selected_colors import color_reduction
from logisticfit import gompertzit
import shutil

start = time.time()

# filename = 'RKOrockinhibitorF1-F11220721F1Merged.tif' #str(sys.argv[1])
# parentdirectory = 'rkorock/0' #str(sys.argv[2])


# parentdirectory = "ibidi"
# filename = "TileScan1A1Merged.tif"


def bgclean(orgfilepath, filename, foldername, debugs=0):
    try:
        os.makedirs("outputs/" + foldername)
    except:
        pass
    try:
        os.makedirs("outputs/" + foldername + '/temp')
        # os.makedirs("outputs/" + foldername + '/meta')
        # os.makedirs("outputs/" + foldername + '/fig')
    except:
        pass

    # print ("cleaning")
    basename = os.path.splitext(filename)[0]
    basename2 = os.path.basename(orgfilepath)
    argcommand = orgfilepath + ' ' + foldername + ' ' + basename + ' ' + basename2
    print(argcommand)
    sig = subprocess.Popen(['ImageJ\ImageJ.exe', '-macro', 'cleaner.ijm', argcommand], shell=True)
    exit_code = sig.wait()
    if exit_code == 0:
        success = 1
        # print("cleaned up")
    else:
        print("messed up cleaning... exiting")
        sys.exit(167)
    # print ("bgremming")

def getcolors(parentdirectory, fromfile):
    if fromfile == 0:
        total_colors_found = int(input("Enter total number of colors"))
        color_inds = list()
        color_inds.append((0, 0, 0))
        print("Black 0,0,0 is added by default")
        for i in range(total_colors_found):
            color_inds.append(np.asarray(input("Enter RGB values seperated by comma eg. 255,255,255 and press enter:")))
        np.savetxt("outputs/" + parentdirectory + "/colors.dat", np.asarray(color_inds).astype(np.uint8), delimiter=',')
    # else:
    #     shutil.copy("resources/" + parentdirectory + "/colors.dat", "outputs/" + parentdirectory + "/colors.dat")


def cleanup(parentdirectory, filename):
    filenames = ["outputs/" + parentdirectory + "/" + filename, "outputs/" + parentdirectory + "/1" + filename]
    for name in filenames:
        img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
        scale_percent = int(2000. / img.shape[1] * 100)  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite(name, resized)


def run(orgfilepath, filename, parentdirectory, fromfile=1, onlyimageprocess = 0):
    # print ("running")
    bgclean(orgfilepath, filename, parentdirectory)
    getcolors(parentdirectory, fromfile)
    cellcounts = color_reduction(filename+'.tif', parentdirectory)
    if onlyimageprocess==0:
        image_gen(parentdirectory)
        # parallel_neigh.execs(parentdirectory)
    retval = 0
    # with open(os.devnull, 'w') as pipe:
    #     process = subprocess.Popen('msmpi/mpiexec.exe -np 10 python parallel_neigh.py ' + parentdirectory, stdout=pipe,
    #                                stderr=pipe, shell=True)
    # retval = process.wait()
    # if retval != 0:
    #     with open(os.devnull, 'w') as pipe:
    #         process = subprocess.Popen('python parallel_neigh.py ' + parentdirectory, shell=True)
    #     retval = process.wait()
    #     print (retval)
    #     gompertzit(parentdirectory, cellcounts)
    #     cleanup(parentdirectory, filename)
    end = time.time()
    # print("Total time taken:", (end - start) / 60.)


# run('D:\\rawdata\\benchmark\\dispersioninvivotest\\dummytest20.tif', '1', 'benchmark\\dispersioninvivotest\\1')
# if __name__ == "__main__":


# imagex = cv2.imread("outputs/" + parentdirectory + "/1" + filename)
# eraser(imagex, parentdirectory, filename, 0)
