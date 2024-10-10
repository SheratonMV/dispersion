import os
import numpy as np
import matplotlib.pyplot as plt


plt.rcParams['svg.fonttype'] = 'none'

def uniquesinlistarray(array):
    lenarr = len(array)
    uniques = list()
    for i in range(lenarr):
        uniques.extend(np.unique(array[i]))
    return np.unique(uniques)

def violin_run(violinplotdata, violinx, title):
    violinplotdatax = list()
    violinplotdatax.append('')
    violinplotdatax.extend(violinx)
    violin_parts = plt.violinplot(violinplotdata, showmeans = True)
    for partname in ('cbars', 'cmins', 'cmaxes', 'cmeans'):
        vp = violin_parts[partname]
        vp.set_edgecolor('red')

    # Make the violin body blue with a red border:
    for vp in violin_parts['bodies']:
        vp.set_facecolor('blue')
        vp.set_edgecolor('red')
        vp.set_alpha(0.3)

    plt.xticks(list(range(len(violinplotdatax))), violinplotdatax)
    plt.xlabel("Rock concentration")
    plt.ylabel("Dispersion score")
    #plt.ylim(,0.6)
    plt.title(title)
    plt.savefig("outputs/dispersion_" + title + ".svg", pad_inches=0.5, bbox_inches='tight', transparent='True')
    plt.clf()

