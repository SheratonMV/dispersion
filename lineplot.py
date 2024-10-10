import numpy as np
import matplotlib.pyplot as plt


def run(data, labels, typeofdata, ylim1=0, ylim2=0):
    c = ['green', 'red', 'blue', 'brown']
    # xvals = list(range(len(labels)-1))
    # plt.rcParams['svg.fonttype'] = 'none'
    # plt.plot(xvals, data[:-1])
    # plt.ylabel("Dispersion score")
    # # plt.ylim(ylim1, ylim2)
    # plt.xlabel("Rock concentration")
    # plt.xticks(xvals, labels[:-1])
    # plt.savefig("outputs/"+typeofdata+"line.svg", fontsize=12, weight='bold')
    # plt.clf()

    xvals = list(range(len(labels)))
    plt.rcParams['svg.fonttype'] = 'none'
    plt.plot(xvals, data)
    plt.ylabel("Dispersion score")
    # plt.ylim(ylim1, ylim2)
    plt.xlabel("Rock concentration")
    plt.xticks(xvals, labels)
    plt.savefig("outputs/" + typeofdata + "line.svg", fontsize=12, weight='bold')
    plt.clf()