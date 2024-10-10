import numpy as np
import matplotlib.pyplot as plt


def run(groups, typenames, data, sddata, xlabel, ylabel, title):
    data = np.array(data)
    sddata = np.array(sddata)
    fig, ax = plt.subplots()
    index = np.arange(len(groups))  # where to put the bars
    bar_width = 1.0 / (len(typenames)) - 0.05
    opacity = 0.5
    error_config = {'ecolor': '0.3'}
    colors = ['green', 'red', 'blue']
    i = 0
    # for j in range(len(typenames)):
    #     print (bar_width)
        # print(j, data[i * 2 + j], index, bar_width, index + bar_width * j)
    subplt = plt.bar(index+ bar_width, data, bar_width, alpha=opacity, color=colors,
                     yerr=sddata,
                     error_kw=error_config, label=typenames, capsize=5)
    # cell_lysate_plt = plt.bar(index, cell_lysate_avg, bar_width, alpha=opacity, color='black', yerr=cell_lysate_sd,
    #                           error_kw=error_config, label='Cell Lysates')
    # media_plt = plt.bar(index + bar_width, media_avg, bar_width, alpha=opacity, color='green', yerr=media_sd,
    #                     error_kw=error_config, label='Media')
    plt.xlabel(xlabel, fontsize=15)
    plt.ylabel(ylabel, fontsize=15)
    plt.title(title)
    plt.xticks(index + bar_width, groups)
    plt.legend()
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    offset = 2

    plt.savefig("outputs/" + title + ".svg", pad_inches=0.5, bbox_inches='tight', transparent='True')
