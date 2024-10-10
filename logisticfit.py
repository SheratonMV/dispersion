#!/usr/bin/python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import math
from fipy import dump
from sklearn.metrics import r2_score



def Function(x, a, b, c):
    # a = upper asymptote
    # b = negative = x axis displacement
    # c = negative = growth rate
    return a * (math.e ** (b * (math.e ** (c * x))))


# parentdirectory = "invivo/ls180"
def gompertzit(parentdirectory, cellcounts):
    xy = dump.read("outputs/" + str(parentdirectory) + "/" + "temp/output.dat")
    xy = np.asarray([j for i in xy for j in i])
    xy = xy.reshape((int(len(xy) / 7), 7))
    # allx = xy[:, 1]
    # ally = xy[:, 6]
    all_params = list()
    allchns = np.unique(xy[:,0])
    for i in range(0, len(allchns)):
        ch = allchns[i]
        chnpts = np.where(xy[:, 0] == ch)
        x = xy[chnpts, 1][0]
        y = xy[chnpts, 6][0]
        pos_correct = np.argsort(x)
        x = x[pos_correct]
        y = y[pos_correct]
        # /np.max(xy[:, :, 6][i])
        # y = np.array([0.0518261, 0.18121327, 0.44985843, 0.72821891, 1.02289896, 1.05564806,  1.03045079, 0.9318427,  1.07446132, 1.13007181, 1.17788089])
        # y = np.array([0.11372649, 0.38921896, 0.78871844, 0.95697276, 1.0491654,  1.06170142, 1.09292877, 1.09767702, 1.14076351, 1.24993808, 1.37764679])
        # cguess = np.log(np.log(y[1] / y[-1]) / np.log(y[-1] / y[0]))
        bguess = -np.log(y[-1] / y[0])
        aguess = y[-1]
        parameters, pcov = curve_fit(Function, x, y, p0=[aguess, bguess, -0.19])
        # Graph data and fit to compare
        ex = np.linspace(min(x), max(x))
        yaj = Function(np.asarray(ex), parameters[0], parameters[1], parameters[2])
        plt.figure(1, figsize=(11, 8.5))
        plt.plot(x, y, 'D')
        plt.plot(ex, yaj, 'r-')
        plt.xlim(min(x), max(x))
        # # plt.ylim(min(yaj), max(yaj) + 0.2)
        plt.xlabel('Order of inclusion')
        plt.ylabel("Mean mix ratio")
        parameters = parameters.tolist()
        parameters.append(r2_score(y, Function(x, parameters[0], parameters[1], parameters[2])))
        parameters.append(cellcounts[i])
        parameters.append(i)
        # print(parameters)
        all_params.append(parameters)
        text_out = str(parameters)
        plt.text(8.5, 6.0, text_out)
        plt.savefig("outputs/" + str(parentdirectory) + "/" + "temp" + "/" + "gompch" + str(ch) + ".tiff")
        plt.clf()
        plt.close()
    np.savetxt("outputs/" + str(parentdirectory) + "/" + "temp" + "/" + "gomparams.dat", np.array(all_params))
    # all_params = np.asarray(all_params)
    # k = (all_params[np.where(
    #     ((all_params[:, 1] > 0.95*np.mean(all_params[:, 1])) & (all_params[:, 1] < -1.5) & (all_params[:, 2] > -0.25) & (all_params[:, 2] < -0.175)))])
    # print (np.mean(k[:, 0]))
# gompertzit("ibidi")