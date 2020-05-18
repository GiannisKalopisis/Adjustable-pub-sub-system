from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def plotAverageValueX(x):
    plt.figure(figsize=(15,10))
    plt.tight_layout()
    seabornInstance.distplot(x)
    plt.show()


def scatter_plot(data, target, feature):
    plt.figure(figsize=(16, 8))
    plt.scatter(data[feature], data[target], edgecolors='none', s=15)
    plt.title("Plot {} per {} ".format(target, feature))
    plt.xlabel("{}".format(feature))
    plt.ylabel("{}".format(target))
    fileName = "./plots/LingerMs_MaxRequestSize/max_latency/" + target.replace(' ', '_').replace('/', '_') + "_" + feature.replace(' ', '_').replace('/', '_') + ".png"
    plt.savefig(fileName, dpi=300, bbox_inches='tight')

