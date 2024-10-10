import os
import shutil
import sys
import time
import glob
import subprocess
import shell_eraser
import pickle


# Disable
def blockprint():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enableprint():
    sys.stdout = sys.__stdout__


# test_only = 0
# if len(sys.argv) > 1:
#     test_only = 1

start = time.time()
# fin = open('source.txt', "rt")
# allpath = "D:\\rawdata\\Tim\\"
# fils = [os.path.join(root, name)
#              for root, dirs, files in os.walk(allpath)
#              for name in files
#              if name.endswith((".tif"))]
# with open('source.dat', 'wb') as handle:
#     pickle.dump(fils, handle)
# counting = -1

# with open('source.dat', 'rb') as handle:
#     orgfilepaths = pickle.load(handle)
# with open('counting.dat', 'rb') as handle:
#     counting = pickle.load(handle)
# for i, orgfilepath in enumerate(orgfilepaths):
#     if i> counting:
neworgfilepath = sys.argv[1]
i = sys.argv[2]
dirpath = sys.argv[3]
starter = time.time()
shell_eraser.run(neworgfilepath, str(i), dirpath,
                 onlyimageprocess=0)
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
with open('counting.dat', 'wb') as handle:
    pickle.dump(i, handle)
print("Total time for ", ':', (time.time() - starter) / 60.)
sys.exit(0)