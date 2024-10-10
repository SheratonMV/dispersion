import os
import numpy as np
from scipy import stats
import violin_plot
import boxplot
import barplot
import lineplot


def find_std(datas):
    a = list()
    for data in datas:
        a.append(np.std(data))
    return a

def find_mean(datas):
    a = list()
    for data in datas:
        a.append(np.mean(data))
    return a
def find_zcut_mean(datas):
    a = list()
    for data in datas:
        zscores = stats.zscore(data, axis=None)
        zscoremean = np.mean(data[np.where(((zscores > -1) & (zscores < 1)))])
        a.append(zscoremean)
    return a

def find_diff(datas1, datas2):
    a = list()
    for data in range(len(datas1)):
        a.append(datas2[data] - datas1[data])
    return a


# parents = ["Da1306042022cad", 'Da1318042022cad', 'Hutu8006042022cad', 'Hutu8018042022cad']
# parents = ["HT55rockimages", 'LS180rockimages', 'DA13rockinh18032022', 'Hutu80rockinh18032022']
parents = ['CMS3']
# titles = ["HT55", 'LS180', 'DA13', 'Hutu80']
titles = ['LS513']
#titles = ['RCM1','SW948', 'Lcolo']
# titles = ["Da13_exp1", 'Da13_exp2', 'Hutu80_exp1', 'Hutu80_exp2']
titlecount = -1
fileprefs = "../../DispersionQuant2/outputs/"
allparents = list()
allcontrols = list()
alldoms = list()
allweaks = list()
for parentdirectory in parents:
    titlecount += 1
    allvals = list()
    pardomvals = list()
    parweakvals = list()
    allexps = list()
    for root, dirs, files in os.walk(fileprefs + parentdirectory):
        path = root.split(os.sep)

        for filer in files:
            paramfilen = ".out"
            if paramfilen in filer:
                typeofexp = os.path.splitext(filer)[0]
                alldisps = np.loadtxt(fileprefs + parentdirectory + os.sep + filer)
                allvals.append(alldisps)
                alldisps = alldisps.reshape(2, -1)
                diffofallsum = np.sum(alldisps, axis=1)[0]-np.sum(alldisps, axis=1)[1]
                if diffofallsum>0:
                    alldisps = np.flip(alldisps)
                    print("flipped", parentdirectory, typeofexp)
                pardomvals.append(alldisps[0])
                parweakvals.append(alldisps[1])

                allcontrols.append(allvals[-1])
                alldoms.append(alldisps[0])
                allweaks.append(alldisps[1])
                allparents.append(titles[titlecount])
                allmeans = np.zeros(2)
                allmedians = np.zeros(2)
                allexps.append(typeofexp)
                for i in range(len(alldisps)):
                    zscores = stats.zscore(alldisps[i], axis=None)
                    zindices = [np.where(((zscores >= -1) & (zscores <= 1)))]
                    zscoremean = np.mean(alldisps[i][zindices])
                    zscoremedian = np.median(alldisps[i][np.where(((zscores >= -1) & (zscores <= 1)))])
                    allmeans[i] = zscoremean
                    allmedians[i] = zscoremedian
                    print(parentdirectory, typeofexp, zscoremean, zscoremedian, len(alldisps[i][zindices][0]))

                finalmean = np.mean(allmeans)
                finalmedian = np.median(allmedians)
                print(parentdirectory, typeofexp, finalmean, finalmedian)
    lineplot.run(find_zcut_mean(pardomvals), allexps, titles[titlecount] + "dom")
    lineplot.run(find_zcut_mean(parweakvals), allexps, titles[titlecount] + "weak")
    lineplot.run(find_zcut_mean(allvals), allexps, titles[titlecount] + "all")
    # violin_plot.violin_run(allvals, allexps, titles[titlecount])
violin_plot.violin_run(alldoms, allexps, titles[titlecount])

boxplot.run(allcontrols, allparents, "Control", 0.0, 0.65)
boxplot.run(alldoms, allparents, "Dominant", 0.0, 0.65)
boxplot.run(allweaks, allparents, "Weak", 0.0, 0.65)
boxplot.run(find_diff(allweaks, alldoms), allparents, "Balance", -0.5, 0.0)
barplot.run(titles, [''], find_mean(allcontrols), find_std(allcontrols), "Cell type", "Dispersion score",
            "Variation of mean dispersion scores")

