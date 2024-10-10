import pickle
import os
import subprocess
import shutil
from fipy import dump
# a = dump.read("D:\\codes\\dispersion\\outputs\\invivo\\SW948319\\1\\temp" + "/" + "output.dat")
venv = dict(os.environ)
allpath = "D://rawdata//benchmark//dispersioninvivotest//"
fils = [os.path.join(root, name)
             for root, dirs, files in os.walk(allpath)
             for name in files
             if name.endswith((".tif"))]
with open('source.dat', 'wb') as handle:
    pickle.dump(fils, handle)
with open('source.dat', 'rb') as handle:
    orgfilepaths = pickle.load(handle)
with open('counting.dat', 'rb') as handle:
    counting = pickle.load(handle)
counting = 0
for i, orgfilepath in enumerate(orgfilepaths):
    if i > counting:
        pp = os.path.dirname(orgfilepath).split("\\")
        pp1 = os.path.dirname(orgfilepath).split("//")
        dirpath = pp1[-2] + "\\" + pp1[-1] + "\\" + str(i)

        if ".tif" in orgfilepath:
            outputdir = 'outputs'+ os.sep + dirpath
        try:
            os.makedirs(outputdir)
        except:
            pass

        shutil.copy("colors.dat", outputdir + "\\" + "colors.dat")

        # try:
        print("Processing:", orgfilepath)
        neworgfilepath = orgfilepath.replace(" ", "").replace("-", "").replace("_", "").replace("//",os.sep)
        os.rename(orgfilepath, neworgfilepath)
        process = subprocess.Popen('python easyrenamer.py ' + neworgfilepath + ' ' + str(i) + ' ' + dirpath, shell=True, env= venv)
        process.wait()