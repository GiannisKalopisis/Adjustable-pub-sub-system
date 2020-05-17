import pandas as pd
import numpy as np
import csv

from general_funcs import *
from parameters_funcs import * 
from print_visualize_funcs import *
from process_csv import *


# filesList= ["../data/1_parameter/Batch_Size.tsv", "../data/1_parameter/Buffer_Memory.tsv", "../data/1_parameter/Linger_Ms.tsv", \
#             "../data/1_parameter/Max_Request_Size.tsv", "../data/1_parameter/Message_Size.tsv", "../data/2_parameters/Batch_Size+Buffer_Memory.tsv",
#             "../data/2_parameters/Batch_Size+Linger_Ms.tsv", "../data/2_parameters/Batch_Size+Max_Request_Size.tsv", "../data/2_parameters/Buffer_Memory+Linger_Ms.tsv", 
#             "../data/2_parameters/Linger_Ms+Max_Request_Size.tsv"]


if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 900)
    
    if len(sys.argv) < 4:
        print("Not enough arguments. Program needs 4(1+3) arguments, but you gave {}.".format(len(sys.argv)))
        sys.exit(1)
    
    target = sys.argv[1]
    feature = sys.argv[2]
    dataFile = sys.argv[3]
    print("Target: {}".format(target))
    print("Feature: {}".format(feature))
    print("File: {}".format(dataFile))

    data = readCSVpd(dataFile)
    # data = data[data['Message Size'] == 500]
    print(data.shape)

    scatter_plot(data, feature, target, dataFile)

    
        






   

   






   

   