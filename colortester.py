import os
import shutil
import sys
import time
import subprocess
import shell_eraser


# Disable
def blockprint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enableprint():
    sys.stdout = sys.__stdout__


start = time.time()
fin = open('source.txt', "rt")
for dir_name in fin:
    dir_name = dir_name.replace("\n", '')
    parentdirectory = dir_name
    resourcedir = 'resources/' + parentdirectory
    outsidedir = 'resources/'
    files = os.listdir(resourcedir)
    start_ind = 0

    for file in files:
        starter = time.time()
        if ".tif" in file:
            outputdir = 'resources/' + parentdirectory + "/" + str(os.path.splitext(file)[0])
            try:
                os.makedirs(outputdir)
            except:
                pass
            changename = file.replace(' ', '')
            changename = changename.replace('_', '')
            shutil.copy(resourcedir + "/" + file, outputdir + "/" + changename)
            shutil.copy(outsidedir + "/" + "colors.dat", outputdir + "/" + "colors.dat")

            # try:
            print("Processing:", changename)
            shell_eraser.run(changename, parentdirectory + "/" + str(os.path.splitext(file)[0]), 1, 1)
            # blockprint()
            # run(changename, parentdirectory + "/" + str(start_ind))
            # with open(os.devnull, 'w') as pipe:
            #     process = subprocess.Popen(
            #         'python .\shell_eraser.py ' + changename + ' ' + parentdirectory + "/" + str(start_ind), stdout=pipe,
            #         stderr=pipe, shell=True)
            # print('python .\shell_eraser.py ' + changename + ' ' + parentdirectory + "/" + str(start_ind))
            # process.wait()

            # except:
            #     enableprint()
            #     print("failed to execute:", changename)
            # enableprint()
            print("Total time for ", changename, ':', (time.time() - starter) / 60.)
            start_ind += 1
print("Total time taken:", (time.time() - start) / 60.)
