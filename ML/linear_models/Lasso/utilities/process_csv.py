import pandas as pd
import numpy as np
import math
import sys
import os


#########################################
#   Read and process file with Pandas   #
#########################################

def readCSVpd(file):
    try:
        data = pd.read_csv(file, sep='\t', header=0, encoding='utf-8')
    except FileNotFoundError:
        print("Couldn't find the file '{}'".format(file))
    return data


def getAverageValuePd(data, average_row):
    return data.iloc[average_row:data.shape[0]:average_row + 1]


def getInputTargetDataPd(data, target_column):

    # input data
    input_columns = data.columns.tolist()
    input_columns.remove(target_column)
    input_data = data[input_columns]
    
    # target data
    target_column = [target_column]
    target_data = data[target_column]

    return input_data, target_data
