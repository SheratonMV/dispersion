import numpy as np
import networkx as nx
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
from matchneighbors import matcher
import matplotlib.pyplot as plt
from pathlib import Path
import glob


def bin_interp(counts, binsval):
    normcumcounts = np.cumsum(counts) / (np.sum(counts))
    splits = [0.5, 0.6, 0.7, 0.8, 0.9]
    disp_score = []
    for split in splits:
        ind = np.argmin((normcumcounts - split) < 0) - 1
        if ind == -1:
            neigh_close =  split / normcumcounts[0]
        else:
            remain = split - normcumcounts[ind]
            neigh_close = binsval[ind] + remain / normcumcounts[ind + 1]
        disp_score.append(neigh_close)
    return disp_score


def write_list_csv(namer, scores, mean_write = 0):
    if mean_write==1:
        filewrite = open("outputs/summary_mean_dispersion_scores.csv", 'a+')
    else:
        filewrite = open("outputs/summary_dispersion_scores.csv", 'a+')
    towrite = namer + ','
    for value in scores:
        towrite += str(round(value, 4)) + ','
    towrite = towrite[:-1] + '\n'
    filewrite.write(towrite)
    filewrite.close()


filewrite = open("outputs/summary_dispersion_scores.csv", 'w')
towrite="File Sheets vs neighbours percentage, 50 , 60, 70, 80, 90\n"
filewrite.write(towrite)
filewrite.close()

filewrite = open("outputs/summary_mean_dispersion_scores.csv", 'w')
towrite="Cell line vs neighbours percentage, 50 , 60, 70, 80, 90\n"
filewrite.write(towrite)
filewrite.close()

all_files = glob.glob("resources/input/*.xlsx")
for filer in all_files:
    namer = filer.split('\\')[1].split('.')[0]
    print (namer)
    xl = pd.ExcelFile(filer)
    sheets = xl.sheet_names
    cell_level = []
    start_sheet = 0
    for sheet in sheets:
        print(start_sheet/len(sheets)*100)
        datain = xl.parse(sheet, header=0)
        try:
            allcolorlabels = np.unique(datain['Name'])
            if 'Nuclei' not in allcolorlabels:

                lencolorlabels = len(np.unique(datain['Class']))
                C1 = np.array(datain['Name'])
                C2 = np.array(datain['Class'])
                for i in range(lencolorlabels):
                    C1[np.where(datain['Name'] == allcolorlabels[i])] = i
                    C2[np.where(datain['Class'] == allcolorlabels[i])] = i
                C = C1 * (np.max(C1) + 1) + C2
                C = C.astype('int')
                X = np.array(datain[datain.keys()[6]])
                Y = np.array(datain[datain.keys()[7]])
                XY = np.concatenate([X[:, None], Y[:, None]], axis=1)
                nbrs = NearestNeighbors(n_neighbors=51, algorithm='ball_tree').fit(XY)
                distances, indices = nbrs.kneighbors(XY)
                retarr = np.zeros_like(X)
                retdistarr = np.zeros_like(X)
                retarr, retdistarr = matcher(distances, indices, C, retarr, retdistarr)
                plt.hist(retarr, bins=int(np.max(retarr) + 1), density=True, cumulative=True)
                # plt.hist(retdistarr*0.634, bins = 30)
                counts, binsval = np.histogram(retarr, bins=int(np.max(retarr) - 1))
                scores = bin_interp(counts, binsval)
                cell_level.append(scores)
                write_list_csv(namer+'_'+sheet,scores)

                # plt.plot(binsval, counts)
                plt.xlim(1, 50)
                plt.xlabel("Heterogenous neighbour order")
                # plt.xlabel("Heterogenous neighbour distance")
                plt.ylabel("Number of cells (Density)")
                # plt.axvline(binsval.mean(), color='r', linestyle='dashed', linewidth=5)
                # plt.ylabel("Number of cells")
                plt.savefig("outputs/allout/" + Path(namer).stem +'_'+ sheet + "_histogram_order_cum.png")
                plt.clf()
                # plt.savefig("outputs/"+Path(namer).stem+"histogram_distance.png")
                start_sheet += 1
        except:
            pass
    cell_level_meanscores = np.zeros((start_sheet, 5))
    for i in range(len(cell_level)):
        cell_level_meanscores[i] = cell_level[i]
    mean_scores = np.mean(cell_level_meanscores, axis=0)
    write_list_csv(namer, mean_scores, 1)