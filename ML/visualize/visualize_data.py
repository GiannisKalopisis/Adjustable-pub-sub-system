import pandas as pd
import numpy as np
import csv
import sys

from utilities.process_csv import *
from utilities.print_visualize_funcs import *

# filesList= ["../data/1_parameter/Batch_Size.tsv", "../data/1_parameter/Buffer_Memory.tsv", "../data/1_parameter/Linger_Ms.tsv", \
#             "../data/1_parameter/Max_Request_Size.tsv", "../data/1_parameter/Message_Size.tsv", "../data/2_parameters/Batch_Size+Buffer_Memory.tsv",
#             "../data/2_parameters/Batch_Size+Linger_Ms.tsv", "../data/2_parameters/Batch_Size+Max_Request_Size.tsv", "../data/2_parameters/Buffer_Memory+Linger_Ms.tsv", 
#             "../data/2_parameters/Linger_Ms+Max_Request_Size.tsv"]


if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 900)
    
    if len(sys.argv) < 3:
        print("Not enough arguments. Program needs 4(1+3) arguments, but you gave {}.".format(len(sys.argv)))
        sys.exit(1)
    
    target = sys.argv[1]
    dataFile = sys.argv[2]
    print("Target: {}".format(target))
    print("File: {}".format(dataFile))

    data = readCSVpd(dataFile)

    # group data 
    # data1 = data[data['Replication Factor'] == 1]
    # data2 = data[data['Replication Factor'] == 2]
    # data5 = data[data['Replication Factor'] == 5]

    # figData = (data1, data2, data5)
    # colors = ("red", "green", "blue")
    # groups = ("Replication Factor 1", "Replication Factor 2", "Replication Factor 5")

    # plt.figure(figsize=(16, 8))
    
    # for figData, color, group in zip(figData, colors, groups):
    #     x, y = figData[feature], figData[target]
    #     plt.scatter(x, y, c=color, edgecolors='none', s=15, label=group)

    features = data.columns.tolist()
    features.remove(target)

    for feature in features:
        scatter_plot(data, target, feature)
    # plt.show()


    
        






   

   






   

   