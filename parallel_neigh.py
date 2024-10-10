# parallel = 0
# try:
#     from mpi4py import MPI
#
#     parallel = 1
# except:
#     pass

import numpy as np
from neighborcalc import neighbors2, chn_totals
from fipy import dump
import sys


def execs(parentdirectory, parallel=0):
    if parallel == 1:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()
        all_vals = list()
        total_channels = chn_totals(parentdirectory)
        if rank == 0:
            filts = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]
            data = [i for i in filts]
            # dividing data into chunks
            chunks = [[] for _ in range(size)]
            for i, chunk in enumerate(data):
                chunks[i % size].append(chunk)
        else:
            data = None
            chunks = None
        data = comm.scatter(chunks, root=0)
        print(rank)
        for filters in data:
            for i in range(total_channels):
                print(i, rank, filters)
                all_vals.append(neighbors2(parentdirectory, i, filters))

        all_vals = comm.allgather(all_vals)
        if rank == 0:
            outputdir = 'outputs/' + parentdirectory + '/temp'
            dump.write(np.asarray(all_vals), outputdir + "/" + "output.dat")
    else:
        total_channels = chn_totals(parentdirectory)
        all_vals = list()
        data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51]
        # print("Work in progress( 0%%)")
        count = 0
        for filters in data:
            for i in range(total_channels):
                msg = "Step 2 : item %i of %i" % (count, len(data) * total_channels)

                count += 1
                sys.stdout.write(msg + chr(8) * len(msg))
                sys.stdout.flush()
                # print(i, filters)
                all_vals.append(neighbors2(parentdirectory, i, filters))
        outputdir = 'outputs/' + parentdirectory + '/temp'
        dump.write(np.asarray(all_vals), outputdir + "/" + "output.dat")
