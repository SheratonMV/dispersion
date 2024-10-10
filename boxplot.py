import matplotlib.pyplot as plt


def run(data, labels, typeofdata, ylim1, ylim2):
    c = ['green', 'red', 'blue', 'brown']
    plt.rcParams['svg.fonttype'] = 'none'
    spacing = [0.25, 0.5, 0.75, 1.0]
    for i in range(len(data)):
        plt.boxplot(data[i], labels=[labels[i]], positions=[spacing[i]], boxprops=dict(color=c[i]),
            capprops=dict(color=c[i]),
            whiskerprops=dict(color=c[i]),
            flierprops=dict(color=c[i], markeredgecolor=c[i]),
            medianprops=dict(color=c[i]))
    plt.ylabel("Dispersion score")
    plt.ylim(ylim1, ylim2)
    plt.savefig("outputs/"+typeofdata+"box.svg", fontsize=12, weight='bold')
    plt.clf()